import bot_util as btl
import datetime as dt

class SC2Mutation:
    def __init__(self):
        self.stages = list(reversed(btl.load_pkl('./data/mutation_stage.pkl')))
        self.factors = btl.load_pkl('./data/mutation_factors.pkl')
        self.template = open('./template/mutation', 'r', encoding='UTF-8').read()
        self.next_week = dt.timedelta(days=7)
    
    def get_recent_stage(self):
        now = dt.datetime.now()
        stage = self._get_stage_by_date(now)
        return self._parse_stage_info(stage)

    def get_next_week_stage(self):
        date = dt.datetime.now() + self.next_week
        stage = self._get_stage_by_date(date)
        return self._parse_stage_info(stage)
    
    def _get_stage_by_date(self, date):
        for stage in self.stages:
            if date > stage['date']:
                return stage
        return None

    def _parse_factors_info(self, factors):
        rtn = list()
        for factor in factors:
            rtn.append('  %s\n      %s' % (factor, self.factors[factor]))
        return '\n'.join(rtn)

    def _parse_stage_info(self, stage):
        if not stage:
            return '我的奴僕還沒有更新異變資訊ヽ(#`Д´)ﾉ'
        return self.template % (stage['stage_name'], stage['map_name'], self._parse_factors_info(stage['factors']))

if __name__ == '__main__':
    sm = SC2Mutation()
    print(sm.get_recent_stage())
    print(sm.get_next_week_stage())