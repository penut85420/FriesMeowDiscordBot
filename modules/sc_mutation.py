import datetime as dt
import json


class SC2Mutation:
    def __init__(self):
        self.next_week = dt.timedelta(days=7)
        self.update_hour = dt.timedelta(hours=1)
        self._load_data()
        self.template = open(
            './template/mutation', 'r', encoding='UTF-8').read()

    def _load_data(self):
        with open('./data/mutation.json', 'r', encoding='UTF-8') as fin:
            data = json.load(fin)

        self.stages = list(reversed(data['stages']))
        for stage in self.stages:
            stage['date'] = dt.datetime.strptime(stage['date'], '%Y/%m/%d')
            stage['date'] += self.update_hour

        self.factors = data['factors']

    def get_recent_stage(self):
        now = dt.datetime.now()
        stage = self._get_stage_by_date(now)
        return self._parse_stage_info(stage)

    def get_left_time(self, stage):
        delta = stage['date']
        delta -= dt.datetime.now()
        minutes = delta.seconds // 60
        hours = minutes // 60
        minutes %= 60
        msg = '%d 天 %d 時 %d 分' % (delta.days, hours, minutes)
        msg = '距離下週異變還有 %s\n\n' % msg
        return msg

    def get_next_week_stage(self):
        date = dt.datetime.now() + self.next_week
        stage = self._get_stage_by_date(date)
        msg = self.get_left_time(stage)
        msg += self._parse_stage_info(stage, title='下週異變')
        return msg

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

    def _parse_stage_info(self, stage, title='本週異變'):
        if not stage:
            return '我的奴僕還沒有更新異變資訊ヽ(#`Д´)ﾉ'
        return self.template % (
            title, stage['stage_name'], stage['map_name'],
            self._parse_factors_info(stage['factors']))


if __name__ == '__main__':
    sm = SC2Mutation()
    print(sm.get_recent_stage())
    print(sm.get_next_week_stage())
