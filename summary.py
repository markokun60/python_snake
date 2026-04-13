import constants

class SummaryValues:
    def __init__(self,name):
        self.name = name
        self.highscore   = {
            constants.AI    :0,
            constants.HUMAN :0
        }
        self.highsize   = {
            constants.AI    :0,
            constants.HUMAN :0
        }
        self.total_games = {
            constants.AI    :0,
            constants.HUMAN : 0
        }
        self.avg_score   = {
            constants.AI    :0.0,
            constants.HUMAN :0.0
    }
        
    def read(self,config):
         for code in [constants.HUMAN,constants.AI]: 
            section = f'{self.name}_{code}'
            self.highscore  [code] = config.getint(section, constants.KEY_HIGH_SCORE , fallback=self.highscore[code] )
            self.total_games[code] = config.getint(section, constants.KEY_TOTAL_GAMES , fallback=self.total_games[code] )
            self.avg_score  [code] = config.getfloat(section, constants.KEY_AVG_SCORE , fallback=self.avg_score[code] )
            self.highsize   [code] = config.getint(section , constants.KEY_HIGH_SIZE , fallback=self.highsize[code] )

    def save(self,config):
        for code in [constants.HUMAN,constants.AI]: 
            section = f'{self.name}_{code}'
            config[section] = {
                constants.KEY_HIGH_SCORE : self.highscore[code],
                constants.KEY_TOTAL_GAMES: self.total_games[code],
                constants.KEY_AVG_SCORE  : self.avg_score[code],
                constants.KEY_HIGH_SIZE  : self.highsize[code]    
            }

    def new_score(self,score,code,size):
        sum_score = self.avg_score[code] * (self.total_games[code]-1)
        sum_score += score
            
        self.avg_score[code] = sum_score / self.total_games[code]

        if size > self.highsize[code]:
            self.highsize[code] = size

        if score > self.highscore[code]:
            self.highscore[code] = score
            return True

        return False
  



