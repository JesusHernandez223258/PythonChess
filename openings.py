def check_open(move_log):
    """
    Verifica los openings más populares
    :param move_log: Lista de movimientos
    :return: Nombre del opening actual
    """
    opening = "Not Found"
    if len(move_log) >= 1:
        if move_log[0].move_id == 6444:  # Peón a e4
            if len(move_log) >= 2:
                if move_log[1].move_id == 1424:  # 2. Move
                    opening = "French Defense"
                elif move_log[1].move_id == 1222:  # 2. Move
                    opening = "Caro-Kann Defense"
                elif move_log[1].move_id == 1333:  # 2. Move
                    opening = "Scandinavian Defense"
                elif move_log[1].move_id == 1232:  # 2. Move
                    opening = "Sicilian Defense"
                    if len(move_log) >= 3:
                        if move_log[2].move_id == 7152:  # 3. Move
                            opening = "Sicilian Def: Closed"
                        elif move_log[2].move_id == 6252:  # 3. Move
                            opening = "Sicilian Def: Alapin Variation"
                elif move_log[1].move_id == 1434:  # 2. Move
                    if len(move_log) >= 3:
                        if move_log[2].move_id == 6545:  # 3. Move
                            opening = "King's Gambit"
                        elif move_log[2].move_id == 7152:  # 3. Move
                            opening = "Vienna Game"
                        elif move_log[2].move_id == 7655:  # 3. Move
                            if len(move_log) >= 4:
                                if move_log[3].move_id == 122:  # 4. Move
                                    if len(move_log) >= 5:
                                        if move_log[4].move_id == 7531:  # 5. Move
                                            opening = "Ruy López Opening"
                                        elif move_log[4].move_id == 7542:  # 5. Move
                                            opening = "Italian Game"
                                        elif move_log[4].move_id == 6343:  # 5. Move
                                            opening = "Scotch Game"
                elif move_log[1].move_id == 1323:  # 2. Move
                    if len(move_log) >= 4:
                        if move_log[2].move_id == 6343 and \
                                move_log[3].move_id == 625:  # 3. y 4. Move
                            opening = "Pirc Defense"
                elif move_log[1].move_id == 625:  # 2. Move
                    opening = "Alekhin's Defense"

        elif move_log[0].move_id == 6343:  # Peón a d4
            if len(move_log) >= 2:
                if move_log[1].move_id == 1535:  # 2. Move
                    opening = "Dutch Defense"
                elif move_log[1].move_id == 1333:  # 2. Move
                    if len(move_log) >= 3:
                        if move_log[2].move_id == 6242:  # 3. Move
                            opening = "Queen's Gambit"
                            if len(move_log) >= 4:
                                if move_log[3].move_id == 1222:  # 4. Move
                                    opening = "Slav Defense"
                        if move_log[2].move_id == 7655:  # 3. Move
                            if len(move_log) >= 4:
                                if move_log[3].move_id == 625:  # 4. Move
                                    if len(move_log) >= 5:
                                        if move_log[4].move_id == 7245:  # 5. Move
                                            opening = "London System"
                elif move_log[1].move_id == 625:  # 2. Move
                    if len(move_log) >= 3:
                        if move_log[2].move_id == 7236:  # 3. Move
                            opening = "Trompowsky Attack"
                        elif move_log[2].move_id == 6242:  # 3. Move
                            if len(move_log) >= 4:
                                if move_log[3].move_id == 1626:  # 4. Move
                                    opening = "King's Indian Defense"
                                    if len(move_log) >= 6:
                                        if move_log[4].move_id == 7152 and \
                                                move_log[5].move_id == 1333:  # 5. y 6. Move
                                            opening = "Grünfeld Defense"
                                elif move_log[3].move_id == 1424:  # 4. Move
                                    if len(move_log) >= 5:
                                        if move_log[4].move_id == 6656:  # 5. Move
                                            opening = "Catalan Opening"
                                        elif move_log[4].move_id == 7655:  # 5. Move
                                            if len(move_log) >= 6:
                                                if move_log[5].move_id == 1121:  # 6. Move
                                                    opening = "Queen's Indian Defense"
                                                elif move_log[5].move_id == 541:  # 6. Move
                                                    opening = "Bogo-Indian Defense"
                                        elif move_log[4].move_id == 7152:  # 5. Move
                                            if len(move_log) >= 6:
                                                if move_log[5].move_id == 541:  # 6. Move
                                                    opening = "Nimzo-Indian Defense"
                                elif move_log[3].move_id == 1232:  # 4. Move
                                    if len(move_log) >= 5:
                                        if move_log[4].move_id == 4333:  # 5. Move
                                            if len(move_log) >= 6:
                                                if move_log[5].move_id == 1131:  # 6. Move
                                                    opening = "Benko Gambit"
                                                elif move_log[5].move_id == 1424:  # 6. Move
                                                    if len(move_log) >= 10:
                                                        if move_log[6].move_id == 7152 and \
                                                                move_log[7].move_id == 2433 and \
                                                                move_log[8].move_id == 4233 and \
                                                                move_log[9].move_id == 1323:  # 7, 8, 9, 10. Move
                                                            opening = "Benoni Defense"
        elif move_log[0].move_id == 7655:
            opening = "Réti Opening"
            if len(move_log) >= 3:
                if move_log[1].move_id == 1333 and move_log[2].move_id == 6656:
                    opening = "King's Indian Attack"
        elif move_log[0].move_id == 6242:
            opening = "English Opening"
        elif move_log[0].move_id == 6545:
            opening = "Bird's Opening"
        elif move_log[0].move_id == 6151:
            opening = "Nimzowitsch-Larsen Atk"
        elif move_log[0].move_id == 6141:
            opening = "Polish Opening"
        elif move_log[0].move_id == 6646:
            opening = "Grob Opening"
        elif move_log[0].move_id == 6656:
            opening = "King's Fianchetto Open"
    return opening
