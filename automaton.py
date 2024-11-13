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
                    #print(f"Estado actual: {self.states[from_state]}, Carácter: {char}, Siguiente estado: {self.states[to_state]}")
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

#Uso del autómata
# automaton = Automaton('grafoFinalFinal.xml')
# input_string = "1. Función cuadrática Esta función toma un número f y devuelve el cuadrado de f + 1. Es útil para transformar valores y calcular cuadrados. n = @(f) (f + 1)^2"  
# valid_sequences = automaton.find_automaton(input_string)

# if valid_sequences:
#     for sequence, start, end in valid_sequences:
#         print(f"Secuencia válida: '{sequence}' desde {start} hasta {end}")
# else:
#     print(f"La cadena '{input_string}' es inválida.")


