import AFND_e
import AFND_eBuilder

def regex_to_afnde(expr): 

    letras = ["a","b","c","e"]
    operadores = ["*",".","|"]

    def parse(expr):
        #Funcion utilizada para pasar la expresion leida a notacion post-fija
        pila_op = []
        pila_final = []
        #para cada simbolo de la ER
        for simbolo in expr :
            #si es una letra va directo a la final
            if simbolo in letras :
                pila_final.append(simbolo)
            
            #si es un simbolo tengo que agregar a la pila final los operadores de mayor o igual precedencia
            # y despues a la pila de operadores el simbolo que acaba de venir
            #precedencia primero * , . , |
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
        print(pila_final)

        return pila_final


    def construir(postfijo):
        #Funcion que construye el afnde
        #postfijo seria la pila de parse

        if postfijo.len() == 0 :
            # caso base vacio, 2 estados sin transicion
            res = AFND_e.AFND_e()
            res.agregar_estado("q_0")
            res.agregar_final("q_f")
            res.establecer_inicial("q_0")
            return res

        sim = postfijo.pop()
        resultado = AFND_e.AFND_e()
        
        if sim in letras:
            #caso base
            afnd = AFND_e.AFND_e()
            length = (postfijo.len() + 1) * 2
            afnd.agregar_estado("q_" + length)
            afnd.agregar_final("q_" + (length - 1))
            afnd.agregar_transicion("q_" + length, sim, "q_" + (length - 1))
        else :
            match sim :
                case  "*" :
                    resultado = kleene(construir(postfijo.pop))
                case "." :
                    resultado = concatenar(construir(postfijo.pop), construir(postfijo.pop))
                case "|" :
                    resultado = pipe(construir(postfijo.pop), construir(postfijo.pop))

        return resultado

    # Operadores
    def concatenar(afnd1, afnd2):
        res = AFND_e.AFND_e()

        res.establecer_inicial(afnd1.inicial)
        res.agregar_transicion(afnd1.finales.pop(), "e", afnd2.inicial)
        res.agregar_final(afnd2.finales.pop())

        return res
    
    def kleene(afnd):
        res = AFND_e.AFND_e()
        length = (postfijo.len() + 1) * 2

        afndAux = AFND_e.AFND_e()
        AFND_eBuilder.copiar(afndAux, afnd)
        
        res.establecer_inicial("q_" + length)
        res.agregar_final("q_" + (length - 1))

        res.agregar_transicion(res.inicial, "e", afndAux.inicial)
        res.agregar_transicion(res.inicial, "e", res.finales.pop())

        res.agregar_transicion(afndAux.finales.pop(), "e", res.finales.pop())
        res.agregar_transicion(afndAux.finales.pop(), "e", afndAux.inicial)

        return res
    
    def pipe(afnd1, afnd2):
        res = AFND_e.AFND_e()
        length = (postfijo.len() + 1) * 2
        
        res.establecer_inicial('q_' + length)
        res.agregar_final('q_' + (length - 1))
        
        res.agregar_transicion(res.inicial, "e", afnd1.inicial)
        res.agregar_transicion(res.inicial, "e", afnd2.inicial)

        

        res.agregar_transicion(next(iter(afnd2.finales)), "e", next(iter(res.finales)))
        res.agregar_transicion(afnd2.finales.pop(), "e", next(iter(res.finales)))

        return res


    postfijo = parse(expr)
    AFND_eBuilder.afnde_to_json(construir(postfijo), f"salidas/test.json")
    return construir(postfijo)
