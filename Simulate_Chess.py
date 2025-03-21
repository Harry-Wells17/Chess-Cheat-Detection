import chess
import chess.engine
import chess.pgn
import random

Stockfish_path = "/opt/homebrew/Cellar/stockfish/17/bin/stockfish"

engine = chess.engine.SimpleEngine.popen_uci(Stockfish_path)

def cheat_in_bad_position(cheater, elo_min, elo_max, out_file):

    board = chess.Board()

    white_elo = random.randint(elo_min, elo_max)
    black_elo = random.randint(elo_min, elo_max)

    # Print the starting board
    #print("\nStarting position:\n")
    #print(board)

    game = chess.pgn.Game()
    game.headers["Event"] = "Cheater Simulation"
    if cheater == 0: # White chosen as cheater
        game.headers["White"] = f"Cheater (ELO: {white_elo})"
        game.headers["Black"] = f"Stockfish (ELO: {black_elo})"
    else:
        game.headers["White"] = f"Stockfish (ELO: {white_elo})"
        game.headers["Black"] = f"Cheater (ELO: {black_elo})"
    game.headers["Result"] = "*"  # Result is unknown until the game ends
    game.headers["WhiteElo"] = f"{white_elo}"
    game.headers["BlackElo"] = f"{black_elo}"

    node = game

    cheater_moves = 0

    while not board.is_game_over():
        if cheater == 0: # White chosen as cheater
            if board.turn:
                engine.configure({"UCI_LimitStrength": False})
                info_before = engine.analyse(board, chess.engine.Limit(depth=20))
                score_before = info_before["score"].white().score()
                #print(score_before)
                if score_before is not None and score_before < 1:
                    #print("CHEATER MOVE")
                    cheater_moves += 1
                    white_move = engine.play(board, chess.engine.Limit(time=1))
                else:
                    engine.configure({"UCI_LimitStrength": True, "UCI_Elo": white_elo})
                    white_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(white_move.move)
                node = node.add_variation(white_move.move)
            else:
                engine.configure({"UCI_LimitStrength": True, "UCI_Elo": black_elo})
                black_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(black_move.move)
                node = node.add_variation(black_move.move)
        else:
            if board.turn:
                engine.configure({"UCI_LimitStrength": True, "UCI_Elo": white_elo})
                white_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(white_move.move)
                node = node.add_variation(white_move.move)
            else:
                engine.configure({"UCI_LimitStrength": False})
                info_before = engine.analyse(board, chess.engine.Limit(depth=20))
                score_before = info_before["score"].black().score()
                #print(score_before)
                if score_before is not None and score_before < 1:
                    #print("CHEATER MOVE")
                    cheater_moves += 1
                    black_move = engine.play(board, chess.engine.Limit(time=1))
                else:
                    engine.configure({"UCI_LimitStrength": True, "UCI_Elo": black_elo})
                    black_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(black_move.move)
                node = node.add_variation(black_move.move)
        #print("\n")
        #print(board)

    game.headers["Result"] = board.result()

    if cheater_moves > 0:
        output_file = open(out_file, "a")
        output_file.write(str(game) + "\n" + "\n")
        output_file.close()

        print("\nPGN Outupt:", game)

        print("\nGame Over. Result:", board.result())  # "1-0", "0-1", or "1/2-1/2"
        print(board)
        print("\nWhite ELO:", white_elo)
        print("Black ELO:", black_elo)
        print("Cheater Moves:", cheater_moves)
    else:
        cheat_in_bad_position(cheater, elo_min, elo_max, out_file)

def cheat_full(cheater, elo_min, elo_max, out_file):

    board = chess.Board()

    white_elo = random.randint(elo_min, elo_max)
    black_elo = random.randint(elo_min, elo_max)

    # Print the starting board
    #print("\nStarting position:\n")
    #print(board)

    game = chess.pgn.Game()
    game.headers["Event"] = "Cheater Simulation"
    if cheater == 0: # White chosen as cheater
        game.headers["White"] = f"Cheater (ELO: {white_elo})"
        game.headers["Black"] = f"Stockfish (ELO: {black_elo})"
    else:
        game.headers["White"] = f"Stockfish (ELO: {white_elo})"
        game.headers["Black"] = f"Cheater (ELO: {black_elo})"
    game.headers["Result"] = "*"  # Result is unknown until the game ends
    game.headers["WhiteElo"] = f"{white_elo}"
    game.headers["BlackElo"] = f"{black_elo}"

    node = game

    cheater_moves = 0

    while not board.is_game_over():
        if cheater == 0: # White chosen as cheater
            if board.turn:
                engine.configure({"UCI_LimitStrength": False})
                #print("CHEATER MOVE")
                cheater_moves += 1
                white_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(white_move.move)
                node = node.add_variation(white_move.move)
            else:
                engine.configure({"UCI_LimitStrength": True, "UCI_Elo": black_elo})
                black_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(black_move.move)
                node = node.add_variation(black_move.move)
        else:
            if board.turn:
                engine.configure({"UCI_LimitStrength": True, "UCI_Elo": white_elo})
                white_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(white_move.move)
                node = node.add_variation(white_move.move)
            else:
                engine.configure({"UCI_LimitStrength": False})
                #print("CHEATER MOVE")
                cheater_moves += 1
                black_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(black_move.move)
                node = node.add_variation(black_move.move)
        #print("\n")
        #print(board)

    game.headers["Result"] = board.result()

    output_file = open(out_file, "a")
    output_file.write(str(game) + "\n" + "\n")
    output_file.close()

    print("\nPGN Outupt:", game)

    print("\nGame Over. Result:", board.result())  # "1-0", "0-1", or "1/2-1/2"
    print(board)
    print("\nWhite ELO:", white_elo)
    print("Black ELO:", black_elo)
    print("Cheater Moves:", cheater_moves)

def cheat_percentage(cheater, percentage, elo_min, elo_max, out_file):

    board = chess.Board()

    white_elo = random.randint(elo_min, elo_max)
    black_elo = random.randint(elo_min, elo_max)

    # Print the starting board
    #print("\nStarting position:\n")
    #print(board)

    game = chess.pgn.Game()
    game.headers["Event"] = "Cheater Simulation"
    if cheater == 0: # White chosen as cheater
        game.headers["White"] = f"Cheater (ELO: {white_elo})"
        game.headers["Black"] = f"Stockfish (ELO: {black_elo})"
    else:
        game.headers["White"] = f"Stockfish (ELO: {white_elo})"
        game.headers["Black"] = f"Cheater (ELO: {black_elo})"
    game.headers["Result"] = "*"  # Result is unknown until the game ends
    game.headers["WhiteElo"] = f"{white_elo}"
    game.headers["BlackElo"] = f"{black_elo}"

    node = game

    cheater_moves = 0
    cheater_chance = percentage / 100

    while not board.is_game_over():
        if cheater == 0: # White chosen as cheater
            if board.turn:
                engine.configure({"UCI_LimitStrength": False})
                if random.random() < cheater_chance:
                    #print("CHEATER MOVE")
                    cheater_moves += 1
                    white_move = engine.play(board, chess.engine.Limit(time=1))
                else:
                    engine.configure({"UCI_LimitStrength": True, "UCI_Elo": white_elo})
                    white_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(white_move.move)
                node = node.add_variation(white_move.move)
            else:
                engine.configure({"UCI_LimitStrength": True, "UCI_Elo": black_elo})
                black_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(black_move.move)
                node = node.add_variation(black_move.move)
        else:
            if board.turn:
                engine.configure({"UCI_LimitStrength": True, "UCI_Elo": white_elo})
                white_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(white_move.move)
                node = node.add_variation(white_move.move)
            else:
                engine.configure({"UCI_LimitStrength": False})
                if random.random() < cheater_chance:
                    #print("CHEATER MOVE")
                    cheater_moves += 1
                    black_move = engine.play(board, chess.engine.Limit(time=1))
                else:
                    engine.configure({"UCI_LimitStrength": True, "UCI_Elo": black_elo})
                    black_move = engine.play(board, chess.engine.Limit(time=1))
                board.push(black_move.move)
                node = node.add_variation(black_move.move)
        #print("\n")
        #print(board)

    game.headers["Result"] = board.result()

    if cheater_moves > 0:
        output_file = open(out_file, "a")
        output_file.write(str(game) + "\n" + "\n")
        output_file.close()

        print("\nPGN Outupt:", game)

        print("\nGame Over. Result:", board.result())  # "1-0", "0-1", or "1/2-1/2"
        print(board)
        print("\nWhite ELO:", white_elo)
        print("Black ELO:", black_elo)
        print("Cheater Moves:", cheater_moves)
    else:
        cheat_percentage(cheater, elo_min, elo_max, out_file)

# Min ELO: 1320
# Max ELO: 3190

output_file1 = "/Users/harry/Documents/Project_Git/hxw285/cheat_in_bad_position_white.pgn"
output_file2 = "/Users/harry/Documents/Project_Git/hxw285/cheat_in_bad_position_black.pgn"
output_file3 = "/Users/harry/Documents/Project_Git/hxw285/cheat_full_white.pgn"
output_file4 = "/Users/harry/Documents/Project_Git/hxw285/cheat_full_black.pgn"
output_file5 = "/Users/harry/Documents/Project_Git/hxw285/cheat_percentage_white.pgn"
output_file6 = "/Users/harry/Documents/Project_Git/hxw285/cheat_percentage_black.pgn"

open(output_file1, "w").close()
open(output_file2, "w").close()
open(output_file3, "w").close()
open(output_file4, "w").close()
open(output_file5, "w").close()
open(output_file6, "w").close()

for i in range(2):
    cheat_in_bad_position(0, 2300, 3190, output_file1)
    cheat_in_bad_position(0, 2200, 2299, output_file1)
    cheat_in_bad_position(0, 2000, 2199, output_file1)
    cheat_in_bad_position(0, 1800, 1999, output_file1)
    cheat_in_bad_position(0, 1600, 1799, output_file1)
    cheat_in_bad_position(0, 1400, 1599, output_file1)
    cheat_in_bad_position(0, 1320, 1399, output_file1)
    cheat_in_bad_position(1, 2300, 3190, output_file2)
    cheat_in_bad_position(1, 2200, 2299, output_file2)
    cheat_in_bad_position(1, 2000, 2199, output_file2)
    cheat_in_bad_position(1, 1800, 1999, output_file2)
    cheat_in_bad_position(1, 1600, 1799, output_file2)
    cheat_in_bad_position(1, 1400, 1599, output_file2)
    cheat_in_bad_position(1, 1320, 1399, output_file2)
    
for i in range(1):
    cheat_full(0, 2300, 3190, output_file3)
    cheat_full(0, 2200, 2299, output_file3)
    cheat_full(0, 2000, 2199, output_file3)
    cheat_full(0, 1800, 1999, output_file3)
    cheat_full(0, 1600, 1799, output_file3)
    cheat_full(0, 1400, 1599, output_file3)
    cheat_full(0, 1320, 1399, output_file3)
    cheat_full(1, 2300, 3190, output_file4)
    cheat_full(1, 2200, 2299, output_file4)
    cheat_full(1, 2000, 2199, output_file4)
    cheat_full(1, 1800, 1999, output_file4)
    cheat_full(1, 1600, 1799, output_file4)
    cheat_full(1, 1400, 1599, output_file4)
    cheat_full(1, 1320, 1399, output_file4)
    
for i in range(2):
    cheat_percentage(0, 75, 2300, 3190, output_file5)
    cheat_percentage(0, 50, 2300, 3190, output_file5)
    cheat_percentage(0, 25, 2300, 3190, output_file5)
    cheat_percentage(0, 75, 2200, 2299, output_file5)
    cheat_percentage(0, 50, 2200, 2299, output_file5)
    cheat_percentage(0, 25, 2200, 2299, output_file5)
    cheat_percentage(0, 75, 2000, 2199, output_file5)
    cheat_percentage(0, 50, 2000, 2199, output_file5)
    cheat_percentage(0, 25, 2000, 2199, output_file5)
    cheat_percentage(0, 75, 1800, 1999, output_file5)
    cheat_percentage(0, 50, 1800, 1999, output_file5)
    cheat_percentage(0, 25, 1800, 1999, output_file5)
    cheat_percentage(0, 75, 1600, 1799, output_file5)
    cheat_percentage(0, 50, 1600, 1799, output_file5)
    cheat_percentage(0, 25, 1600, 1799, output_file5)
    cheat_percentage(0, 75, 1400, 1599, output_file5)
    cheat_percentage(0, 50, 1400, 1599, output_file5)
    cheat_percentage(0, 25, 1400, 1599, output_file5)
    cheat_percentage(0, 75, 1320, 1399, output_file5)
    cheat_percentage(0, 50, 1320, 1399, output_file5)
    cheat_percentage(0, 25, 1320, 1399, output_file5)
    cheat_percentage(1, 75, 2300, 3190, output_file6)
    cheat_percentage(1, 50, 2300, 3190, output_file6)
    cheat_percentage(1, 25, 2300, 3190, output_file6)
    cheat_percentage(1, 75, 2200, 2299, output_file6)
    cheat_percentage(1, 50, 2200, 2299, output_file6)
    cheat_percentage(1, 25, 2200, 2299, output_file6)
    cheat_percentage(1, 75, 2000, 2199, output_file6)
    cheat_percentage(1, 50, 2000, 2199, output_file6)
    cheat_percentage(1, 25, 2000, 2199, output_file6)
    cheat_percentage(1, 75, 1800, 1999, output_file6)
    cheat_percentage(1, 50, 1800, 1999, output_file6)
    cheat_percentage(1, 25, 1800, 1999, output_file6)
    cheat_percentage(1, 75, 1600, 1799, output_file6)
    cheat_percentage(1, 50, 1600, 1799, output_file6)
    cheat_percentage(1, 25, 1600, 1799, output_file6)
    cheat_percentage(1, 75, 1400, 1599, output_file6)
    cheat_percentage(1, 50, 1400, 1599, output_file6)
    cheat_percentage(1, 25, 1400, 1599, output_file6)
    cheat_percentage(1, 75, 1320, 1399, output_file6)
    cheat_percentage(1, 50, 1320, 1399, output_file6)
    cheat_percentage(1, 25, 1320, 1399, output_file6)

engine.close()