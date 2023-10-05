import random

def roll_dice(n=2, sides=6):
    return sum(random.randint(1, sides) for _ in range(n))


def simulate_game(team1, team2, automate_game):
    team1.set_opponent(team2)
    team2.set_opponent(team1)

    rodada = 1
    while True:
        print("------------------------------------------------------------------------")
        print(f"RODADA {rodada}")

        if rodada % 6 == 0:
            # Incrementar o bonus do apanhador a cada 6 rodadas
            team1.increment_seeker_bonus()
            team2.increment_seeker_bonus()

        for player_type in ['artilheiros', 'batedores', 'goleiro', 'apanhador']:
            print(f"Turno {player_type}:")
            team1_skip = False
            team2_skip = False
            if team1.players_remaining[player_type] == 0:
                team1_skip = True
            if team2.players_remaining[player_type] == 0:
                team2_skip = True

            dice_result_team1 = roll_dice()
            dice_result_team2 = roll_dice()

            if player_type == 'apanhador':
                if team1.seeker_has_priority:
                    game_over_team1 = team1.round_scorer(player_type, dice_result_team1, team1_skip, automate_game)
                    game_over_team2 = team2.round_scorer(player_type, dice_result_team2, team2_skip, automate_game)
                else:
                    game_over_team2 = team2.round_scorer(player_type, dice_result_team2, team2_skip, automate_game)
                    game_over_team1 = team1.round_scorer(player_type, dice_result_team1, team1_skip, automate_game)
                if not team1.snitch_caugth and not team2.snitch_caugth:
                    team1.determine_priority()
            else:     
                game_over_team1 = team1.round_scorer(player_type, dice_result_team1, team1_skip, automate_game)
                game_over_team2 = team2.round_scorer(player_type, dice_result_team2, team2_skip, automate_game)

            if game_over_team1 or game_over_team2:
                print("\nFim de jogo!")
                print(f"Placar final: {team1.name}: {team1.score}, {team2.name}: {team2.score}")
                if team1.score > team2.score:
                    print(f"\tCasa {team1.name} vence!")
                else:
                    print(f"\tCasa {team2.name} vence!")
                return
            elif team1.players_remaining['apanhador'] == 0 and team2.players_remaining['apanhador'] == 0:
                print("\nFim de jogo, todos os apanhadores foram derrubados!")
                print(f"Placar final: {team1.name}: {team1.score}, {team2.name}: {team2.score}")
                if team1.score > team2.score:
                    print(f"\tCasa {team1.name} vence!")
                else:
                    print(f"\tCasa {team2.name} vence!")
                return
            print("\n")

        crowd_result_team1 = roll_dice()
        crowd_result_team2 = roll_dice()
        print("Turno das torcidas")
        team1.crowd_cheers(crowd_result_team1, automate_game)
        team2.crowd_cheers(crowd_result_team2, automate_game)
        print(f"\nPlacar -> {team1.name}: {team1.score} | {team2.name}: {team2.score}")
        input(f"\nRodada: {rodada} Pressione ENTER para o próximo turno.\n")

        rodada += 1
        
def select_team(opcoes):
    while True:
        print("\n".join(f"\t{i+1} - {team}" for i, team in enumerate(opcoes)))
        choice = input()
        if choice.isdigit() and 1 <= int(choice) <= len(opcoes):
            selected_team = opcoes[int(choice) - 1]
            opcoes.remove(selected_team)
            return selected_team
        else:
            print("Por favor, escolha uma opção válida.")