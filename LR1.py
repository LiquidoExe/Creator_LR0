from Lector import lector
import pdb;
pdb.set_trace()

class LR1:
	#Constructor de la clase
	#lt = lista de terminales
	#ln = lista de no terminales
	#dc = diccionario de terminales-reglas
	def __init__(self,lt,ln,dc,cod):
		self.lt=lt
		self.ln=ln
		self.dc=dc
		self.cod=cod
		self.inv_cod()
		print("TERMINALES:",lt)
		print("NO TERMINALES:",ln)
		print("CÓDIGO:",self.cod)
		print("\nDICCIONARIO DE REGLAS:")
		for key in self.dc.keys():
			print(key,"\t",self.dc.get(key))
		#print("CÓDIGO:",self.inv_cod)
	#Función para invertir las llaves y los valores del dic cod.
	def inv_cod(self):
		inv_map = {v: k for k, v in self.cod.items()}
		self.inv_cod=inv_map
	#Función para obtener el First:
	#El First() se forma con el primer símbolo de una producción:
	#1. Si el símbolo es terminal, el first del símbolo es el mismo símbolo.
	#2. Si el símbolo es no terminal se vuelve a aplicar el first sobre el nuevo no terminal.
	#s = símbolo
	#c = conjunto
	#r = regla
	#res = conjunto resultado
	def first(self,s,res):
		#print("First de",s,res)
		#Caso terminal:
		if s not in res and s in self.lt:
			res.append(s)
			return
		#caso no terminal:
		c=self.dc.get(s)
		if c != None:
			for r in c:
				if len(r) > 0:
					s_aux=r[0]
					if s != s_aux:
						self.first(s_aux,res)
		else:
			print("Noone.")
	#Función para obtener el Follow:
	#El Follow() de un no terminal es el First() de el símbolo que está
	#delante de él en los lados derechos.
	#Si no hay un símbolo delante, entonces se agrega el Follow del lado izquierdo.
	#Si épsilon está en el resultado se calcula el follow del lado izquierdo.
	#s = símbolo
	#c = conjunto
	#r = regla
	#k = llave
	#p = posición
	#res = conjunto resultado
	def follow(self,s,res):
		print("Follow de",s,res)
		#Si se busca el follow del primer símbolo de la gramática se agrega '$'
		if s == 0 and -1 not in res:
			res.append(-1)

		for k in self.dc.keys():
			c=self.dc.get(k)
			for r in c:
				if s in r:
					p=r.index(s)
					#Si es el último elemento se calcula el follow del lado izquierdo:
					if p == len(r)-1 and k != s:
						self.follow(k,res)
					#Si s tiene otro símbolo adelante se calcula el first de lo que sigue:
					elif p < len(r)-1:
						print("Símbolo delante:",r[p+1])
						self.first(r[p+1],res)
	#Función mover:
	#c = conjunto
	#r = regla
	#s = simbolo
	#c_f = conjunto final
	#p_s = posicion de s
	#c_r = copia de regla
	def mover(self,c,s):
		#print("moviendo",c,"con",s)
		c_f=[]
		for tupla in c:
			r=tupla[0]
			if self.a_mover(r,s) != None:
				c_f.append([self.a_mover(r,s),tupla[1].copy()])
		#print("Resultado:",c_f)
		return(c_f)
	#Función auxiliar de mover():
	#c_r = copia de la regla
	#p = posición
	#r = regla
	#s = simbolo
	def a_mover(self,r,s):
		try:
			p=r.index(0)
		except ValueError:
			return r.copy()

		if p < len(r)-1 and r[p+1] == s:
			#print("ingreso",r)
			c_r=r.copy()
			c_r.remove(0)
			c_r.insert(p+1,0)
			#print("regreso",c_r)
			return c_r
		else:
			return None
	#Devolver todas las posiciones de un símbolo:
	#r = regla
	#s = símbolo
	#c_r = conjunto resultado
	def buscar_s(self,r,s):
		c_r=[]
		for p in range(len(r)):
			if s == r[p]:
				c_r.append(p)
		return c_r
	#Función cerradura() se obtienen dos elementos en una lista
	#[[Elementos de la cerradura][Elementos de los first]]
	#C_E = Conjunto de reglas externo a la función.
	def cerradura(self,c_e):
		c_final=[]
		p_final=0
		#Para cada conjunto en c_e
		for tupla in c_e:
			if tupla not in c_final:
				c_final.append(tupla)
			#Iteraciones sobre el número de estados.
			while p_final < len(c_final):
				c=c_final[p_final]
				#c=[[estados],[firsts]]
				estados=c[0]
				firsts=c[1]
				p=estados.index(0)
				#print("Lista",c,"en posicion",p)
				if p < len(estados)-1:
					if p < len(estados)-2:
						n_firsts=[]
						self.first(estados[p+2],n_firsts)
					else:
						n_firsts=firsts.copy()

					if estados[p+1] in self.ln:
						for r in self.dc.get(estados[p+1]):
							r_c=r.copy()
							r_c.insert(0,0)

							if [r_c,n_firsts] not in c_final:
								c_final.append([r_c,n_firsts])

				p_final+=1
				#print(c_final)
		#print("\t\tCerradura:",c_final)
		return c_final
	#Función ir_a, la unión de la función mover y cerradura:
	#c = conjunto
	#s = símbolo
	def ir_a(self,c,s):
		return self.cerradura(self.mover(c,s))
	#Función para utilizar ir_a en los diferentes conjuntos:
	#self.pool = donde se guardan todos los conjuntos resultantes i(x)
	#p = posicion
	#s = simbolo
	#c = conjunto simple
	#d_r = diccionario de relaciones contiene los conjuntos que salieron de otro conjunto.
	#r = relaciones
	def crear(self):
		self.pool=[]
		d_r={}
		self.pool.append(self.cerradura([[[0,1],[-1]]]))
		p=0

		while p < len(self.pool):
			print("Analizando el conjunto I("+str(p)+"):")
			for s in self.posteriores(self.pool[p]):
				print("\tBuscando el símbolo",s,":")
				c=self.ir_a(self.pool[p],s)
				if c not in self.pool:
					self.pool.append(c)
				print(p,"\t",self.inv_cod.get(s),"\t",self.pool.index(c))
				r=(p,s)
				d_r.setdefault(r,self.pool.index(c))
			p+=1

		print(self.pool)
		print("POOL DE CONJUNTOS:")
		for conjunto in self.pool:
			print("[",end="")
			for regla in conjunto:
				print("[",end="")
				for p in range(len(regla[0])):
					if regla[0][p] == 0:
						print(".",end="")
					else:
						print(self.inv_cod.get(regla[0][p]), end="")
				print("]",end="")
			print("]")

		print("DICCIONARIO DE DESPLAZAMIENTO:")
		for key in d_r.keys():
			print("[",key[0],self.inv_cod.get(key[1]),d_r.get(key),"]",end="\t")
		print("TOTAL",len(d_r))
		self.diccionario_desplazamiento=d_r
	#Función para obtener los símbolos antes del punto:
	#c = conjunto de reglas.
	def posteriores(self,c):
		post=[]
		for tupla in c:
			r=tupla[0]
			if r.index(0) < len(r)-1 and r[r.index(0)+1] not in post:
				post.append(r[r.index(0)+1])
		return post
	#Función para obtener las reglas que necesitan first y follow
	#l_r = lista de reglas originales por posición
	#p = posición
	#c = conjunto
	#r = regla
	def reglas(self):
		d=self.inv_dc()
		l_r=self.val_list()
		dic={}
		#print(l_r)
		for p in range(len(self.pool)):
			c=self.pool[p]
			for tupla in c:
				r=tupla[0]
				if r[len(r)-1] == 0:
					r_c=r.copy()
					r_c.pop()
					print(p,l_r.index(r_c),end=" ")
					#self.p_lista(self.follow(d.get(tuple(r_c)),[]))
					print("")

					for simb in tupla[1]:
						dic.setdefault((p,simb),l_r.index(r_c))

		print("DICCIONARIO DE REDUCCIÓN:\n")
		for key in dic.keys():
			print("[",key[0],self.inv_cod.get(key[1]),dic.get(key),"]",end="\t")
		print("TOTAL",len(dic))
		print("TOTAL",len(dic))
		self.diccionario_reduccion=dic
	#Función que invierte las llaves y los valores del diccionario dc:
	def inv_dc(self):
		inv={}
		for key in self.dc.keys():
			for r in self.dc.get(key):
				inv.setdefault(tuple(r),key)

		return inv
	#Fución que regresa una lista de los valores del diccionario:
	def val_list(self):
		l_r=[]
		for key in self.dc.keys():
			for l in self.dc.get(key):
				l_r.append(l)
		return l_r
	#Función para evaluar la cadena:
	def evaluar(self,l):
		print("CADENA",l)
		reglas=self.val_list()
		busqueda=self.inv_dc()
		print("REGLAS:",reglas)
		pila=[-1,0]
		error=0

		while not error:
			self.p_operaciones(pila)
			self.p_lista(l)
			s=l.pop(0)

			if (pila[-1],s) in self.diccionario_desplazamiento:
				print("DESPLAZAMIENTO",self.diccionario_desplazamiento.get((pila[-1],s)))
				pila.append(s)
				pila.append(self.diccionario_desplazamiento.get((pila[-2],s)))

			elif (pila[-1],s) in self.diccionario_reduccion:
				print("REDUCCION",self.diccionario_reduccion.get((pila[-1],s)))
				if (pila[-1],s) == (1,-1):
					print("Cadena aceptada.")
					return
				pos=self.diccionario_reduccion.get((pila[-1],s))
				cardinalidad=len(reglas[pos])*2

				for n in range(cardinalidad):
					pila.pop()

				pila.append(busqueda.get(tuple(reglas[pos])))

				if (pila[-2],pila[-1]) in self.diccionario_desplazamiento:
					pila.append(self.diccionario_desplazamiento.get((pila[-2],pila[-1])))

				elif (pila[-2],pila[-1]) in self.diccionario_reduccion:
					pila.append(self.diccionario_reduccion.get((pila[-2],pila[-1])))

				l.insert(0,s)
			else:
				print("ERROR")
				return
	def p_lista(self,l):
		print("[",end="")
		for e in l:
			print(self.inv_cod.get(e),end=" ")
		print("]",end="")
	def p_operaciones(self,l):

		print("[",end="")
		for p in range(0,len(l),2):
			print(self.inv_cod.get(l[p]),l[p+1],end=" ")
		print("]",end="")

#Menú:
reglas=lector()
tabla=LR1(reglas.lt,reglas.ln,reglas.diccionario,reglas.conjunto_reglas)
tabla.crear()
tabla.reglas()
r=reglas.convertir_cadena("aadad")
tabla.evaluar(r)
