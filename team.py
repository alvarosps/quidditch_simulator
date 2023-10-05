import random

ARTILHEIROS = 'artilheiros'
BATEDORES = 'batedores'
GOLEIRO = 'goleiro'
APANHADOR = 'apanhador'
RESERVAS = 'reservas'

SUCCESS_MIN_ROLL = 10
GREATER_SUCCESS_MIN_ROLL = 13
PARTIAL_SUCCESS_MIN_ROLL = 7
FAILURE_MAX_ROLL = 6

SNITCH_CAUGHT_MIN_ROLL = 15
SNITCH_CAUGHT_BONUS = 50

SCORE_DIFFERENCE_MIN_CHASER_BONUS = 80

class Team:
    def __init__(self, name, players, crowd, opponent=None, initial_score=0):
        self.name = name
        self.players = {
            ARTILHEIROS: players[ARTILHEIROS],
            BATEDORES: players[BATEDORES],
            GOLEIRO: players[GOLEIRO],
            APANHADOR: players[APANHADOR],
        }
        self.reservas = players[RESERVAS]
        self.crowd = crowd
        self.opponent = opponent
        self.score = initial_score
        self.initialize_game_state()
        
    def initialize_game_state(self):
        self.crowd_bonus_next_round = {ARTILHEIROS: 0, BATEDORES: 0, GOLEIRO: 0, APANHADOR: 0}
        self.players_remaining = {ARTILHEIROS: 6, BATEDORES: 4, GOLEIRO: 2, APANHADOR: 2}
        self.snitch_spotted = False
        self.last_seeker_roll = 0
        self.seeker_has_priority = False
        self.seeker_bonus = 0
        self.snitch_caugth = False

    def set_initial_score(self, initial_score):
        self.score = initial_score

    def set_opponent(self, opponent):
        self.opponent = opponent

    def increment_seeker_bonus(self):
        self.seeker_bonus += 1

    def round_scorer(self, player_type, dice_result, should_skip, automate_game):
        if self.players_remaining[player_type] > 0:
            total = self.calculate_total(player_type, dice_result)
            is_game_over = self.handle_player_actions(player_type, total, should_skip, automate_game)
            print(f"Score da equipe {self.name}: {self.score}")
            return is_game_over
        else:
            print(f"Equipe {self.name} não tem mais {player_type}, SKIP")
            return False

    def calculate_total(self, player_type, dice_result):
        skill = self.players[player_type]['modificador'] if player_type != ARTILHEIROS and player_type != BATEDORES else 0
        total = dice_result + skill + self.crowd_bonus_next_round[player_type]
        if player_type == APANHADOR:
            total += self.seeker_bonus
        return total
    
    def handle_player_actions(self, player_type, total, should_skip, automate_game):
        if should_skip:
            print(f"Nao existem mais {player_type} na equipe, pulando jogada")
            return
        if self.players_remaining[player_type] == 0:
            # safeguard, should_skip estava falhando as vezes
            print(f"Equipe {self.name} não tem mais {player_type}, SKIP")
            return
        if player_type == ARTILHEIROS:
            is_game_over = self.handle_chasers(total)
        elif player_type == BATEDORES:
            is_game_over = self.handle_beaters(total, automate_game)
        elif player_type == GOLEIRO:
            is_game_over = self.handle_keeper(total)
        elif player_type == APANHADOR:
            is_game_over = self.handle_seeker(total)
        return is_game_over
    
    def handle_chasers(self, total):
        for chaser in self.players[ARTILHEIROS]:
            skill = chaser['modificador']
            total_chaser = total + skill + self.crowd_bonus_next_round[ARTILHEIROS]
            print(f"\tArtilheiro {chaser['nome']} rolou {total_chaser}")
            
            if total_chaser <= FAILURE_MAX_ROLL:
                self.score -= 10
                if self.score < 0:
                    self.score = 0
            elif PARTIAL_SUCCESS_MIN_ROLL <= total_chaser < SUCCESS_MIN_ROLL:
                pass
            elif SUCCESS_MIN_ROLL <= total_chaser < GREATER_SUCCESS_MIN_ROLL:
                self.score += 10
            elif total_chaser >= GREATER_SUCCESS_MIN_ROLL:
                self.score += 20
        self.crowd_bonus_next_round[ARTILHEIROS] = 0
        return False

    def handle_beaters(self, total, automate_game):
        scores = []
        for beater in self.players[BATEDORES]:
            skill = beater['modificador']
            beater_total = total + skill + self.crowd_bonus_next_round[BATEDORES]
            print(f"\tBatedor {beater['nome']} rolou {beater_total}")
            scores.append(beater_total)
        if len(self.players[BATEDORES]) == 2 and ((scores[0] >= GREATER_SUCCESS_MIN_ROLL and scores[1] >= SUCCESS_MIN_ROLL) or (scores[0] >= SUCCESS_MIN_ROLL and scores[1] >= GREATER_SUCCESS_MIN_ROLL)) or len(self.players[BATEDORES]) == 1 and scores[0] >= GREATER_SUCCESS_MIN_ROLL:
            if automate_game == False:
                position_to_knock_out = self.select_position_to_knock_out()
            else:
                position_to_knock_out = self.random_select_position()
            self.score += 20
            print(f"\tOs batedores do time {self.name} derrubou o {position_to_knock_out} do time {self.opponent.name}!")
            self.opponent.knock_out(position_to_knock_out)
        elif len(self.players[BATEDORES]) == 2 and scores[0] <= FAILURE_MAX_ROLL and scores[1] <= FAILURE_MAX_ROLL:
            self.opponent.score += 20
        elif len(self.players[BATEDORES]) == 1:
            if scores[0] >= 13:
                position = self.random_select_position()
                self.opponent.crowd_bonus_next_round[position] -= 1
                self.score += 10
            elif scores[0] >= 10:
                self.score += 10
            elif scores[0] >= 7:
                pass
            else:
                self.opponent.score += 10

        self.crowd_bonus_next_round[BATEDORES] = 0
        return False

    def handle_keeper(self, total):
        if total >= GREATER_SUCCESS_MIN_ROLL:
            self.score += 10
            if self.opponent.score >= 20:
                self.opponent.score -= 20
            else:
                self.opponent.score = 0
        elif total >= SUCCESS_MIN_ROLL:
            self.score += 10
            if self.opponent.score > 0:
                self.opponent.score -= 10
            else:
                self.opponent.score = 0
        elif total >= PARTIAL_SUCCESS_MIN_ROLL:
            if self.opponent.score > 0:
                self.opponent.score -= 10
            else:
                self.opponent.score = 0
        else:
            self.opponent.score += 10
        return False

    def handle_seeker(self, total):
        if not self.snitch_spotted:
            if total >= SUCCESS_MIN_ROLL:
                self.snitch_spotted = True
                print(f"\tA equipe {self.name} visualizou o pomo de ouro!")
                self.seeker_has_priority = True
        else:
            if total >= SNITCH_CAUGHT_MIN_ROLL:
                if self.score + SNITCH_CAUGHT_BONUS > self.opponent.score:
                    print(f"\tO apanhador da casa {self.name} capturou o pomo de ouro!")
                    self.score += 50
                    self.snitch_caugth = True
                    return True
                elif self.score + SCORE_DIFFERENCE_MIN_CHASER_BONUS > self.opponent.score:
                    self.crowd_bonus_next_round[ARTILHEIROS] += 1
                else:
                    self.crowd_bonus_next_round[APANHADOR] += 3
                    
            elif total >= SUCCESS_MIN_ROLL:
                self.crowd_bonus_next_round[APANHADOR] += 2
            elif total >= PARTIAL_SUCCESS_MIN_ROLL:
                self.crowd_bonus_next_round[APANHADOR] += 1
            elif total <= FAILURE_MAX_ROLL:
                self.crowd_bonus_next_round[APANHADOR] -= 2
        self.last_seeker_roll = total
        return False

    def determine_priority(self):
        if self.last_seeker_roll > self.opponent.last_seeker_roll:
            self.seeker_has_priority = True
            self.opponent.seeker_has_priority = False
            print(f"Apanhador {self.players[APANHADOR]['nome']} do time {self.name} ganhou prioridade para o próximo turno.")
        elif self.last_seeker_roll < self.opponent.last_seeker_roll:
            self.seeker_has_priority = False
            self.opponent.seeker_has_priority = True
            print(f"Apanhador {self.opponent.players[APANHADOR]['nome']} do time {self.opponent.name} ganhou prioridade para o próximo turno.")
        else:
            if self.players[APANHADOR]['modificador'] > self.opponent.players[APANHADOR]['modificador']:
                self.seeker_has_priority = True
                self.opponent.seeker_has_priority = False
                print(f"Apanhador {self.players[APANHADOR]['nome']} do time {self.name} ganhou prioridade para o próximo turno.")
            elif self.players[APANHADOR]['modificador'] < self.opponent.players[APANHADOR]['modificador']:
                self.seeker_has_priority = False
                self.opponent.seeker_has_priority = True
                print(f"Apanhador {self.opponent.players[APANHADOR]['nome']} do time {self.opponent.name} ganhou prioridade para o próximo turno.")

    def knock_out(self, player_type):
        if self.players_remaining[player_type] > 0:
            # self.players[player_type] = max(0, self.players[player_type] - 1)
            if player_type == ARTILHEIROS:
                # select which random chaser will be knocked out
                random_idx = random.randint(0, len(self.players[ARTILHEIROS]) - 1)
                print(f"\t\tArtilheiro {self.players[ARTILHEIROS][random_idx]['nome']} foi derrubado")
                removed_player = self.players[ARTILHEIROS].pop(random_idx)
                if len(self.reservas[ARTILHEIROS]) > 0:
                    print(f"\t\tArtilheiro {self.reservas[ARTILHEIROS][0]['nome']} vai entrar!")
                    new_player = self.reservas[ARTILHEIROS].pop(0)
                    self.players[ARTILHEIROS].append(new_player)
                else:
                    print(f"\t\tNão tem mais artilheiros da {self.name} na reserva!")
            elif player_type == BATEDORES:
                random_idx = random.randint(0, len(self.players[BATEDORES]) - 1)
                print(f"\t\tBatedor {self.players[BATEDORES][random_idx]['nome']} foi derrubado")
                removed_player = self.players[BATEDORES].pop(random_idx)
                if len(self.reservas[BATEDORES]) > 0:
                    print(f"\t\tBatedor {self.reservas[BATEDORES][0]['nome']} vai entrar!")
                    new_player = self.reservas[BATEDORES].pop(0)
                    self.players[BATEDORES].append(new_player)
                else:
                    print(f"\t\tNão tem mais batedores da {self.name} na reserva!")
            else:
                print(f"\t\t{player_type} {self.players[player_type]['nome']} foi derrubado!")
                self.players[player_type] = None
                if len(self.reservas[player_type]) > 0:
                    print(f"\t\t{self.reservas[player_type][0]['nome']} vai entrar!")
                    new_player = self.reservas[player_type].pop(0)
                    self.players[player_type] = new_player
                else:
                    print(f"\t\tNão tem mais {player_type} da {self.name} na reserva!")

            self.players_remaining[player_type] -= 1

    def select_position_to_knock_out(self):
        print(f"({self.name}) você pode derrubar um jogador adversário, escolha qual!")
        print("Digite o número entre 1 e 4 para escolher a posição a derrubar:")
        print("\t1: artilheiros")
        print("\t2: batedores")
        print("\t3: goleiro")
        print("\t4: apanhador")
        chasers_left = self.players_remaining[ARTILHEIROS]
        beaters_left = self.players_remaining[BATEDORES]
        keepers_left = self.players_remaining[GOLEIRO]
        seekers_left = self.players_remaining[APANHADOR]
        
        choice = input()
        if choice == '1' and chasers_left > 0:
            return ARTILHEIROS
        elif choice == '2' and beaters_left > 0:
            return BATEDORES
        elif choice == '3' and keepers_left > 0:
            return GOLEIRO
        elif choice == '4' and seekers_left > 0:
            return APANHADOR
        else:
            print("Opção invalida ou a posição não tem mais jogadores disponíveis, selecione novamente.")
            return self.select_position_to_knock_out()
        
    def random_select_position(self):
        random_dice = sum(random.randint(1, 8) for _ in range(1))
        chasers_left = self.players_remaining[ARTILHEIROS]
        beaters_left = self.players_remaining[BATEDORES]
        keepers_left = self.players_remaining[GOLEIRO]
        seekers_left = self.players_remaining[APANHADOR]

        chasers_condition = range(1, chasers_left + 1)
        beaters_condition = range(chasers_left + 1, chasers_left + beaters_left + 1)
        keepers_condition = range(chasers_left + beaters_left + 1, chasers_left + beaters_left + keepers_left + 1)
        seekers_condition = range(chasers_left + beaters_left + keepers_left + 1, chasers_left + beaters_left + keepers_left + seekers_left + 1)

        if random_dice in chasers_condition:
            return ARTILHEIROS
        elif random_dice in beaters_condition:
            return BATEDORES
        elif random_dice in keepers_condition:
            return GOLEIRO
        elif random_dice in seekers_condition:
            return APANHADOR
        else:
            positions_available = []
            if chasers_left > 0:
                print(f"0 - Artilheiro ({chasers_left} restantes)")
                positions_available.append(ARTILHEIROS)
            if beaters_left > 0:
                print(f"1 - Batedor ({beaters_left} restantes)")
                positions_available.append(BATEDORES)
            if keepers_left > 0:
                print(f"2 - Goleiro ({keepers_left} restantes)")
                positions_available.append(GOLEIRO)
            if seekers_left > 0:
                print(f"3 - Apanhador ({seekers_left} restantes)")
                positions_available.append(APANHADOR)
            print("Digite qualquer outra opção para ser aleatorio.")
            position_idx = input("Selecione a posição para derrubar")
            if position_idx == '0' and ARTILHEIROS in positions_available:
                return ARTILHEIROS
            elif position_idx == '1' and BATEDORES in positions_available:
                return BATEDORES
            elif position_idx == '2' and GOLEIRO in positions_available:
                return GOLEIRO
            elif position_idx == '3' and APANHADOR in positions_available:
                return APANHADOR
            else:
                i = random.randint(0, len(positions_available) - 1)
                return positions_available[i]


    def select_position_to_increment(self):
        print(f"({self.name}) Sua torcida está dando +1 para o apanhador e mais uma posição, escolha qual!")
        print("Digite o número entre 1 e 3 para escolher a posição a aumentar:")
        print("\t1: artilheiros")
        print("\t2: batedores")
        print("\t3: goleiro")
        choice = input()
        if choice == '1':
            return ARTILHEIROS
        elif choice == '2':
            return BATEDORES
        elif choice == '3':
            return GOLEIRO
        else:
            return self.select_position_to_increment()

    def crowd_cheers(self, dice_result, automate_game):
        total = dice_result + self.crowd
        print(f"Roll da torcida da {self.name}: {total}")
        if total >= SUCCESS_MIN_ROLL:
            self.crowd_bonus_next_round[APANHADOR] += 1
            if automate_game == False: 
                position = self.select_position_to_increment()
            else:
                position = self.random_select_position()
            self.opponent.crowd_bonus_next_round[position] += 1
        elif total >= PARTIAL_SUCCESS_MIN_ROLL:
            self.crowd_bonus_next_round[APANHADOR] += 1