import chess
import chess.engine
import chess.pgn
import csv

Stockfish_path = "/opt/homebrew/Cellar/stockfish/17/bin/stockfish"

engine = chess.engine.SimpleEngine.popen_uci(Stockfish_path)

pgn_path = "/Users/harry/Documents/Project_Git/hxw285/ficsgamesdb_202502_standard_movetimes_13887.pgn"
backup_pgn_path = "/Users/harry/Documents/Project_Git/hxw285/ficsgamesdb_202501_standard_nomovetimes_409001.pgn"
backup_pgn_path2 = "/Users/harry/Documents/Project_Git/hxw285/ficsgamesdb_202412_standard_nomovetimes_409010.pgn"
cheat_pgn_1_white = "/Users/harry/Documents/Project_Git/hxw285/cheat_in_bad_position_white.pgn"
cheat_pgn_1_black = "/Users/harry/Documents/Project_Git/hxw285/cheat_in_bad_position_black.pgn"
cheat_pgn_2_white = "/Users/harry/Documents/Project_Git/hxw285/cheat_full_white.pgn"
cheat_pgn_2_black = "/Users/harry/Documents/Project_Git/hxw285/cheat_full_black.pgn"
cheat_pgn_3_white = "/Users/harry/Documents/Project_Git/hxw285/cheat_percentage_white.pgn"
cheat_pgn_3_black = "/Users/harry/Documents/Project_Git/hxw285/cheat_percentage_black.pgn"

elo_array = []
cpl_array = []
blunder_array = []
match_array = []
cheater_array = []

def parse_pgn(input_pgn_path, elo_min, elo_max, output_pgn):

    input_pgn = open(input_pgn_path)

    counter = 0

    for game in input_pgn:

        if counter > 9:
            break

        game = chess.pgn.read_game(input_pgn)

        if game is not None and game.headers["Result"] != "1/2-1/2" and ((int(game.headers["WhiteElo"]) > elo_min and int(game.headers["WhiteElo"]) < elo_max) and (int(game.headers["BlackElo"]) > elo_min) and int(game.headers["BlackElo"]) < elo_max):
                
            board = game.board()

            node = game
                
            for move in game.mainline_moves():
                board.push(move)
                node = node.add_variation(move)

            output_file = open(output_pgn, "a")
            output_file.write(str(game) + "\n" + "\n")
            output_file.close()

            counter += 1
            print(counter)

    if counter < 10 :
        backup_pgn = open(backup_pgn_path)

        for game in backup_pgn:

            if counter > 9:
                break

            game = chess.pgn.read_game(backup_pgn)

            if game is not None and game.headers["Result"] != "1/2-1/2" and ((int(game.headers["WhiteElo"]) > elo_min and int(game.headers["WhiteElo"]) < elo_max) and (int(game.headers["BlackElo"]) > elo_min) and int(game.headers["BlackElo"]) < elo_max):
                
                board = game.board()

                node = game
                    
                for move in game.mainline_moves():
                    board.push(move)
                    node = node.add_variation(move)

                output_file = open(output_pgn, "a")
                output_file.write(str(game) + "\n" + "\n")
                output_file.close()

                counter += 1
                print(counter)

    if counter < 10 :
        backup_pgn2 = open(backup_pgn_path2)

        for game in backup_pgn2:

            if counter > 9:
                break

            game = chess.pgn.read_game(backup_pgn2)

            if game is not None and game.headers["Result"] != "1/2-1/2" and ((int(game.headers["WhiteElo"]) > elo_min and int(game.headers["WhiteElo"]) < elo_max) and (int(game.headers["BlackElo"]) > elo_min) and int(game.headers["BlackElo"]) < elo_max):
                
                board = game.board()

                node = game
                    
                for move in game.mainline_moves():
                    board.push(move)
                    node = node.add_variation(move)

                output_file = open(output_pgn, "a")
                output_file.write(str(game) + "\n" + "\n")
                output_file.close()

                counter += 1
                print(counter)

def analyse_single_game(input_pgn):
    
    open_pgn = open(input_pgn)
    game = chess.pgn.read_game(open_pgn)

    board = game.board()

    white_move_count = 0
    white_stockfish_match = 0
    black_move_count = 0
    black_stockfish_match = 0

    white_total_cpl = 0
    black_total_cpl = 0
    white_blunders = 0
    black_blunders = 0

    white_endgame_moves = 0
    black_endgame_moves = 0
    white_endgame_match = 0
    black_endgame_match = 0

    for move in game.mainline_moves():

        if board.turn:
            white_move_count += 1
            info_before = engine.analyse(board, chess.engine.Limit(depth=20))
            best_move = info_before["pv"][0]
            score_before = info_before["score"].white().score()

            board.push(move)

            info_after = engine.analyse(board, chess.engine.Limit(depth=20))
            score_after = info_after["score"].white().score()
        else:
            black_move_count += 1
            info_before = engine.analyse(board, chess.engine.Limit(depth=20))
            best_move = info_before["pv"][0]
            score_before = info_before["score"].black().score()

            board.push(move)

            info_after = engine.analyse(board, chess.engine.Limit(depth=20))
            score_after = info_after["score"].black().score()

        if score_after is not None:
            cpl = abs(score_before - score_after)
            if board.turn:
                black_total_cpl += cpl
                if cpl > 200:
                    black_blunders += 1
                if move == best_move:
                    black_stockfish_match += 1
                if len(board.piece_map()) <= 7:
                    black_endgame_moves += 1
                    if move == best_move:
                        black_endgame_match += 1
            else:
                white_total_cpl += cpl
                if cpl > 200:
                    white_blunders += 1
                if move == best_move:
                    white_stockfish_match += 1
                if len(board.piece_map()) <= 7:
                    white_endgame_moves += 1
                    if move == best_move:
                        white_endgame_match += 1

        print("\nBoard after Player's move:\n")
        print(board)

    white_average_cpl = white_total_cpl / white_move_count if white_move_count > 0 else 0
    black_average_cpl = black_total_cpl / black_move_count if black_move_count > 0 else 0
    white_blunder_rate = white_blunders / white_move_count * 100
    black_blunder_rate = black_blunders / black_move_count * 100
    white_stockfish_match_percent = white_stockfish_match / white_move_count * 100
    black_stockfish_match_percent = black_stockfish_match / black_move_count * 100
    white_endgame_accuracy = (white_endgame_match / white_endgame_moves * 100) if white_endgame_moves > 0 else 0
    black_endgame_accuracy = (black_endgame_match / black_endgame_moves * 100) if black_endgame_moves > 0 else 0

    print("\nGame Over. Result:", board.result())

    print("\nWhite Report:")
    print("ELO:", game.headers["WhiteElo"])
    print("Average Centipawn Loss:", white_average_cpl)
    print(f"Blunder Rate: {white_blunder_rate}%")
    print(f"Stockfish Match %: {white_stockfish_match_percent}%")
    print(f"Endgame Accuracy %: {white_endgame_accuracy}%")

    print("\nBlack Report:")
    print("ELO:", game.headers["BlackElo"])
    print("Average Centipawn Loss:", black_average_cpl)
    print(f"Blunder Rate: {black_blunder_rate}%")
    print(f"Stockfish Match %: {black_stockfish_match_percent}%")
    print(f"Endgame Accuracy %: {black_endgame_accuracy}%")

def analyse_games(input_pgn, white_cheater, black_cheater):

    input_pgn_open = open(input_pgn)

    for game in input_pgn_open:

        game = chess.pgn.read_game(input_pgn_open)

        if game is not None:
            
            board = game.board()

            # Print the starting board
            #print("\nStarting position:\n")
            #print(board)

            white_move_count = 0
            white_stockfish_match = 0
            black_move_count = 0
            black_stockfish_match = 0

            white_total_cpl = 0
            black_total_cpl = 0
            white_blunders = 0
            black_blunders = 0

            white_endgame_moves = 0
            black_endgame_moves = 0
            white_endgame_match = 0
            black_endgame_match = 0

            for move in game.mainline_moves():

                if board.turn:
                    white_move_count += 1
                    info_before = engine.analyse(board, chess.engine.Limit(depth=20))
                    best_move = info_before["pv"][0]
                    score_before = info_before["score"].white().score()

                    board.push(move)

                    info_after = engine.analyse(board, chess.engine.Limit(depth=20))
                    score_after = info_after["score"].white().score()
                else:
                    black_move_count += 1
                    info_before = engine.analyse(board, chess.engine.Limit(depth=20))
                    best_move = info_before["pv"][0]
                    score_before = info_before["score"].black().score()

                    board.push(move)

                    info_after = engine.analyse(board, chess.engine.Limit(depth=20))
                    score_after = info_after["score"].black().score()

                if score_before and score_after is not None:
                    cpl = abs(score_before - score_after)
                    if board.turn:
                        black_total_cpl += cpl
                        if cpl > 200:
                            black_blunders += 1
                        if move == best_move:
                            black_stockfish_match += 1
                        if len(board.piece_map()) <= 7:
                            black_endgame_moves += 1
                            if move == best_move:
                                black_endgame_match += 1
                    else:
                        white_total_cpl += cpl
                        if cpl > 200:
                            white_blunders += 1
                        if move == best_move:
                            white_stockfish_match += 1
                        if len(board.piece_map()) <= 7:
                            white_endgame_moves += 1
                            if move == best_move:
                                white_endgame_match += 1

                #print("\nBoard after Player's move:\n")
                #print(board)

            white_average_cpl = white_total_cpl / white_move_count if white_move_count > 0 else 0
            black_average_cpl = black_total_cpl / black_move_count if black_move_count > 0 else 0
            white_blunder_rate = white_blunders / white_move_count * 100 if white_move_count > 0 else 0
            black_blunder_rate = black_blunders / black_move_count * 100 if black_move_count > 0 else 0
            white_stockfish_match_percent = white_stockfish_match / white_move_count * 100 if white_move_count > 0 else 0
            black_stockfish_match_percent = black_stockfish_match / black_move_count * 100 if black_move_count > 0 else 0
            white_endgame_accuracy = (white_endgame_match / white_endgame_moves * 100) if white_endgame_moves > 0 else 0
            black_endgame_accuracy = (black_endgame_match / black_endgame_moves * 100) if black_endgame_moves > 0 else 0

            print("\nGame Over. Result:", game.headers["Result"])

            print("\nWhite Report:")
            print("ELO:", game.headers["WhiteElo"])
            print("Average Centipawn Loss:", white_average_cpl)
            print(f"Blunder Rate: {white_blunder_rate}%")
            print(f"Stockfish Match %: {white_stockfish_match_percent}%")
            print(f"Endgame Accuracy %: {white_endgame_accuracy}%")

            print("\nBlack Report:")
            print("ELO:", game.headers["BlackElo"])
            print("Average Centipawn Loss:", black_average_cpl)
            print(f"Blunder Rate: {black_blunder_rate}%")
            print(f"Stockfish Match %: {black_stockfish_match_percent}%")
            print(f"Endgame Accuracy %: {black_endgame_accuracy}%")

            elo_array.append(int(game.headers["WhiteElo"]))
            cpl_array.append(white_average_cpl)
            blunder_array.append(white_blunder_rate)
            match_array.append(white_stockfish_match_percent)
            cheater_array.append(white_cheater)

            elo_array.append(int(game.headers["BlackElo"]))
            cpl_array.append(black_average_cpl)
            blunder_array.append(black_blunder_rate)
            match_array.append(black_stockfish_match_percent)
            cheater_array.append(black_cheater)

            rows = [[int(game.headers["WhiteElo"]), white_average_cpl, white_blunder_rate, white_stockfish_match_percent, white_cheater], 
                    [int(game.headers["BlackElo"]), black_average_cpl, black_blunder_rate, black_stockfish_match_percent, black_cheater] 
            ]

            output_file = open("/Users/harry/Documents/Project_Git/hxw285/training_data.csv", "a")
            writer = csv.writer(output_file)
            writer.writerows(rows)
            output_file.close()

            print("\nELO array:", elo_array)
            print("CPL array:", cpl_array)
            print("Blunder array:", blunder_array)
            print("Stockfish Match array:", match_array)
            print("Cheater array:", cheater_array)

# ELO boundaries are based on https://www.chess.com/terms/elo-rating-chess

output_file = "/Users/harry/Documents/Project_Git/hxw285/real_games.pgn"

open(output_file, "w").close() # Clears file

parse_pgn(pgn_path, 2299, 3191, output_file)
parse_pgn(pgn_path, 2199, 2300, output_file)
parse_pgn(pgn_path, 1999, 2200, output_file)
parse_pgn(pgn_path, 1799, 2000, output_file)
parse_pgn(pgn_path, 1599, 1800, output_file)
parse_pgn(pgn_path, 1399, 1600, output_file)
parse_pgn(pgn_path, 1319, 1400, output_file)


analyse_games(output_file, 0, 0)
analyse_games(cheat_pgn_1_white, 1, 0)
analyse_games(cheat_pgn_1_black, 0, 1)
analyse_games(cheat_pgn_2_white, 1, 0)
analyse_games(cheat_pgn_2_black, 0, 1)
analyse_games(cheat_pgn_3_white, 1, 0)
analyse_games(cheat_pgn_3_black, 0, 1)

analyse_single_game("/Users/harry/Downloads/Magnus-Carlsen_vs_Jose-Carlos-Ibarra-Jerez_2025.01.07.pgn")

engine.close()