import xml.etree.ElementTree as ET
import re

class Automaton:
    def __init__(self, xml_file):
        self.states = {}
        self.transitions = []
        self.initial_state = None
        self.final_states = set()
        self.parse_xml(xml_file)

    def parse_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for state in root.find('automaton').findall('state'):
            state_id = state.get('id')
            state_name = state.get('name')
            is_initial = state.get('initial') == 'true'
            is_final = state.get('final') == 'true'
            
            self.states[state_id] = state_name
            if is_initial:
                self.initial_state = state_id
            if is_final:
                self.final_states.add(state_id)

        for transition in root.find('automaton').findall('transition'):
            from_state = transition.find('from').text
            to_state = transition.find('to').text
            read_value = transition.find('read').text
            self.transitions.append((from_state, to_state, read_value))



    def valid_transition(self, current_state, char):
        for (from_state, to_state, read_value) in self.transitions:
            if from_state == current_state:
                if self.match_transition(read_value, char):
                    print(f"Estado actual: {self.states[from_state]}, Carácter: {char}, Siguiente estado: {self.states[to_state]}")
                    return to_state
        return None



    def match_transition(self, read_value, char):
        if read_value == '[" "↹]':
            return char in [' ', '\t']


        if read_value.startswith('[') and read_value.endswith(']'):
            range_pattern = read_value[1:-1]
            return bool(re.match(f"[{range_pattern}]", char))
        
        return read_value == char
    


    def find_automaton(self, input_string):
        valid_sequences = []
        current_sequence = ""
        current_state = self.initial_state
        initial_char = None


        for i in range(len(input_string)):
            char = input_string[i]
            #print(f" position array:{input_string[i]}")
            next_state = self.valid_transition(current_state, char)


            if next_state is None:
                if current_state in self.final_states and current_sequence:
                    valid_sequences.append((current_sequence, initial_char, i - 1))
                
                current_state = self.initial_state
                current_sequence = ""
                initial_char = None
            else:
                if current_sequence == "":
                    initial_char = i

                current_sequence += char
                current_state = next_state

        if current_state in self.final_states and current_sequence:
            valid_sequences.append((current_sequence, initial_char, len(input_string) - 1))

        return valid_sequences

# Uso del autómata
# automaton = Automaton('grafoFinalFinal.xml')
# input_string = "hola"  
# valid_sequences = automaton.find_automaton(input_string)

# if valid_sequences:
#     for sequence, start, end in valid_sequences:
#         print(f"Secuencia válida: '{sequence}' desde {start} hasta {end}")
# else:
#     print(f"La cadena '{input_string}' es inválida.")



def test_valid_inputs():
    input_string = [
        "k = @(j , l , s , i , p , a) j^2 + sin(j);",
        "w = @(o) (sin(o) + cos(o)) / 2;",
        "f = @(a) a + exp(a);",
        "g = @(b) b^2 - 7;",
        "h = @(c) 3 * sin(c);",
        "i = @(h) log(h) / (h + 1);",
        "m = @(x, y) x ^ 3  +  y ^ 3   -  3 * x  * y;",
        "parabola = @(x) a*x.^2 + b*x + c;",
        "f = @(x) x.^2 + 3.*x - 5;",
        "g = @(x) (x + 1) - log(x);",
        "h = @(x, y) x.^2 + y.^2 - 2.*x.*y;",
        "sqr = @(x) x.^2;",
        "sinfunc = @(x) sin(x) + cos(x);",
        "expfunc = @(t) exp(t) - 1;",
        "k = @(a, b, c) a.*b + log(c);",
        "f = @(x) (x.^2 + x.*3) + 90;",
        "vecop = @(x, y) (x.^2 + y.^2) - 20;"
    ]
    valid_sequence = []
    automaton = Automaton('automaton2.xml')
    for string in input_string:
        valid_sequence.append(automaton.find_automaton(string))
    print("Valid inputs:")
    print(valid_sequence)
    

#test_valid_inputs()

def test_invalid_inputs():
    input_string = [
        "k = @(j , l , s , i , p , a)) j^2 + sen(j);",   # Paréntesis de cierre extra
        "w = @((o) (sen(o) + cos(o)) / 2;",            # Paréntesis de apertura extra
        "f = @(a) a ++ exp(a);",                       # Doble operador "+"
        "g = @(b) b^^2 - 7;",                          # Doble operador "^"
        "h = @@(c) 3 * sen(c);",                       # Doble "@"
        "i = @(hh) log(hh) / (h + 1);",                # Doble letra en variable
        "m = @(x, y) x ^ 3  ++  y ^ 3   -  3 * x  * y;", # Operador "+" duplicado
        "z = @(u) u * (sin(u) - cos(u)))(;",            # Paréntesis de apertura sin cierre
        "q = @(t t) exp(t) / (1 + t);",                # Variable repetida en definición
        "y = @(r, s) (r ^ ^ 2 + s ^ 2) * sen(r);"      # Operador "^" repetido
        "k = @(j , l , s , i , p , a)) j^2 + sen(j);",
        "w = @((o) (sen(o) + cos(o)) / 2;",
        "f = @(a) a ++ exp(a);",
        "g = @(b) b^^2 - 7;"
        "h = @@(c) 3 * sen(c);"
        "h = @@(c) 3 * sen(c)"
    ]
    invalid_sequence = []
    automaton = Automaton('grafoFinalFinal.xml')
    for string in input_string:
        invalid_sequence.append(automaton.find_automaton(string))
    print("Invalid inputs:")
    print(invalid_sequence)

#test_invalid_inputs()

def test_valid_long_inputs():
    input_string = [
        "k = @(j, l, s, i, p, a) (j^2 + sen(j)) / (cos(j) + exp(l) - log(s) + p * a);",
        "w = @(o, u, v) (sen(o) + cos(u)) / (1 + exp(v) ^ 2 + log(u));",
        "f = @(a, b, c) (a + b ^ 2 - c) / sen(a)+ cos(c);",
        "g = @(x, y, z) x ^ 3 + y ^ 3 + z ^ 3 - 3 * x * y * z;",
        "h = @(p, q) (3 * sen(p) + cos(q)) * (exp(q) / log(q));",
        "m = @(x, y, z, w) (x + y + z) ^ 2 + (sen(x) * cos(y) / log(z))- exp(w);",
        "z = @(a, b, c, d) (a * b - c) + sen(d)^ 2 + cos(a)/ exp(b);",
        "q = @(u, v, w) (exp(u) + log(v)) / (sen(w) + cos(w))* (u ^ 2 + v ^ 2);",
        "y = @(x, y, z, w, v) (x ^ 2 + y ^ 2) * sen(z)+ (cos(w) / log(v));"
    ]
    valid_sequence = []
    automaton = Automaton('grafoFinalFinal.xml')
    for string in input_string:
        valid_sequence.append(automaton.find_automaton(string))
    print("Valid long inputs:")
    print(valid_sequence)

#test_valid_long_inputs()
