import AFND_e
import AFND_eBuilder

def regex_to_afnde(expr): 

    letras = ["a","b","c","e"]
    operadores = ["*",".","|"]

    def parse(expr):
        # Funcion utilizada para pasar la expresion leida a notacion post-fija
        pila_op = []
        pila_final = []

        # Para cada simbolo de la ER
        for simbolo in expr :

            # Si es una letra va directo a la final
            if simbolo in letras :
                pila_final.append(simbolo)
            
            # si es un simbolo tengo que agregar a la pila final los operadores de mayor o igual precedencia
            # y despues a la pila de operadores el simbolo que acaba de venir
            # precedencia primero * , . , |
            else :
                aux = []
                match simbolo :
                    case  "*" :
                        while pila_op != []:
                            sim = pila_op.pop()
                            if sim != simbolo:
                                aux.append(sim)
                            else:
                                pila_final.append(sim)
                    
                    case "." :
                        while pila_op :
                            sim = pila_op.pop()
                            if sim == "|":
                                aux.append(sim)
                            else:
                                pila_final.append(sim)
                    
                    case "|" :
                        while pila_op :
                            pila_final.append(pila_op.pop())      
                
                aux.reverse()
                aux.append(simbolo)
                pila_op = aux
        
        while pila_op :
            pila_final.append(pila_op.pop())
        #print(pila_final)

        return pila_final

    # De una lista, construye el AFND-e
    def construir(postfijo):
        # Funcion que construye el afnde

        if len(postfijo) == 0 :
            # Caso borde vacio, 2 estados sin transicion
            # Igual al parecer nunca va a llegar a este caso, ya que expr = "" dijeron que no es valida en los foros
            # Queda implementada por las dudas xd
            afnd = AFND_e.AFND_e()
            inicio = f"q_{AFND_eBuilder.nuevo_estado()}"
            fin = f"q_{AFND_eBuilder.nuevo_estado()}"

            afnd.establecer_inicial(inicio)
            afnd.agregar_final(fin)

            return afnd
        
        # Pila auxiliar que va almacenando los AFNDs que voy construyendo
        pila_aux = []

        for simbolo in postfijo:

            if simbolo in letras:
                # caso base de un literal (a,b,c,e), construyo un AFND-e simple
                afnd = AFND_e.AFND_e()
                inicio = f"q_{AFND_eBuilder.nuevo_estado()}"
                fin = f"q_{AFND_eBuilder.nuevo_estado()}"

                afnd.establecer_inicial(inicio)
                afnd.agregar_final(fin)
                afnd.agregar_transicion(inicio, simbolo, fin)
                pila_aux.append(afnd)

            elif simbolo == "*":
                afnd = pila_aux.pop()
                pila_aux.append(kleene(afnd))

            elif simbolo == ".":
                afnd2 = pila_aux.pop()
                afnd1 = pila_aux.pop()
                pila_aux.append(concatenar(afnd1, afnd2))

            elif simbolo == "|":
                afnd2 = pila_aux.pop()
                afnd1 = pila_aux.pop()
                pila_aux.append(pipe(afnd1, afnd2))
                
        return pila_aux.pop()

    # Operadores

    # Dado un AFND-e de (r) y otro de (s), devuelve otro AFND-e que hace (r.s)
    def concatenar(afnd1, afnd2):
        # inicializo mi nuevo afnd-e
        res = AFND_e.AFND_e()

        # copio los afnds que ya tengo
        AFND_eBuilder.copiar(res, afnd1)
        AFND_eBuilder.copiar(res, afnd2)
    
        # almaceno los finales de los otros afnd-e (obs: son unicos por mas de que vengan en una lista, len(afnd.finales) = 1)
        finalAfnd1 = afnd1.finales.pop()
        finalAfnd2 = afnd2.finales.pop()

        # determino inicial, final y la transicion
        res.establecer_inicial(afnd1.inicial)
        res.agregar_transicion(finalAfnd1, "e", afnd2.inicial)
        res.agregar_final(finalAfnd2)

        return res
    
    # Dado un AFND-e de (r), devuelve otro AFND-e que hace (r)*
    def kleene(afnd):
        # inicializo mi nuevo afnd-e
        res = AFND_e.AFND_e()

        # copio los afnds que ya tengo
        AFND_eBuilder.copiar(res, afnd)
        
        # almaceno los finales de los otros afnd-e
        finalAfnd = afnd.finales.pop()

        # determino mi estado inicial y final nuevos
        inicial = f"q_{AFND_eBuilder.nuevo_estado()}"
        final = f"q_{AFND_eBuilder.nuevo_estado()}"

        # determino las nuevas transiciones
        res.establecer_inicial(inicial)
        res.agregar_final(final)

        res.agregar_transicion(res.inicial, "e", afnd.inicial)
        res.agregar_transicion(res.inicial, "e", final)

        res.agregar_transicion(finalAfnd, "e", final)
        res.agregar_transicion(finalAfnd, "e", afnd.inicial)

        return res
    
    # Dado un AFND-e de (r) y otro de (s), devuelve otro AFND-e que hace (r|s)
    def pipe(afnd1, afnd2):
        # inicializo mi nuevo afnd-e
        res = AFND_e.AFND_e()

        # copio los afnds que ya tengo
        AFND_eBuilder.copiar(res, afnd1)
        AFND_eBuilder.copiar(res, afnd2)

        # almaceno los finales de los otros afnd-e
        finalAfnd1 = afnd1.finales.pop()
        finalAfnd2 = afnd2.finales.pop()
        
        # determino mi estado inicial y final nuevos
        inicial = f"q_{AFND_eBuilder.nuevo_estado()}"
        final = f"q_{AFND_eBuilder.nuevo_estado()}"

        # determino las nuevas transiciones
        res.establecer_inicial(inicial)
        res.agregar_final(final)
        
        res.agregar_transicion(res.inicial, "e", afnd1.inicial)
        res.agregar_transicion(res.inicial, "e", afnd2.inicial)

        res.agregar_transicion(finalAfnd1, "e", final)
        res.agregar_transicion(finalAfnd2, "e", final)

        return res

    # Construccion final
    postfijo = parse(expr)
    #AFND_eBuilder.afnde_to_json(construir(postfijo), f"salidas/test.json")
    return construir(postfijo)
