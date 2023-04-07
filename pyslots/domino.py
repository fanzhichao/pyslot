import numpy as np

all_poker_list = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5],[6, 6], \
                  [0, 0], [0, 2], [0, 3], [0, 4], [0, 5], [0,6], \
                  [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], \
                  [2, 3], [2, 4], [2, 5], [2, 6], \
                  [3, 4], [3, 5], [3, 6],  \
                  [4, 5], [4, 6], [5, 6]]
class Player:
    def __init__(self, name, pokerlist):
        self.name = name
        self.poker_list = pokerlist
        self.pass_poker_list = []

    def get_name(self):
        return self.name

    def get_poker_list(self):
        return self.poker_list

    # 判断两个牌是否能相连
    def is_hoker(self, poker1, poker2):
        if len(poker1) == 0 or len(poker2) == 0:
            return True
        if poker1[0] == poker2[0] or poker1[0] == poker2[1] \
            or poker1[1] == poker2[1] or poker1[1] == poker2[0]:
            return True
        return False
    # 看一下是否有可出的牌
    def get_next_pokers(self, poker_start, poker_end):
        start_result = []
        end_result = []
        for v in self.poker_list:
            if self.is_hoker(v, poker_start):
                start_result.append(v)
            if self.is_hoker(v, poker_end):
                end_result.append(v)
        return [start_result, end_result]

    def choose_poker_with_state(self,start_result, end_result, table_poker, player_list):
        result = []
        for v in start_result:
            result = [v, 0]
            return result
        for v in end_result:
            result = [v, 1]
            return result
        return result

    def chupai(self, table_poker, player_list):
        res = self.get_next_pokers(table_poker.getStartPoker(), table_poker.getEndPoker())
        poker_with_state = self.choose_poker_with_state(res[0], res[1], table_poker, player_list)
        if len(poker_with_state) > 0:
            table_poker.chupai(poker_with_state[0],poker_with_state[1])
            self.poker_list.remove(poker_with_state[0])
            return 1
        else:
            return 0
    def print_left_poker(self):
        print(self.name+"还剩 " +  str(self.poker_list))

    def has_no_poker(self):
        if len(self.poker_list) > 0:
            return False
        else:
            return True

    def suan_fen(self):
        res = 0
        for v in self.poker_list:
            res = res+ v[0] +v[1]
        return res

    def get_win_result(self):
        if self.name == 'A':
            return [1,0,0,0]
        elif self.name == 'B':
            return [0,1,0,0]
        elif self.name == 'C':
            return [0,0,1,0]
        elif self.name == 'D':
            return [0,0,0,1]
        else:
            return [0, 0, 0, 0]
    def add_pass_poker(self, poker_index_list):
        self.pass_poker_list = self.pass_poker_list + poker_index_list

    def get_pass_poker(self):
        return self.pass_poker_list
class CleverPlayer(Player):

    # top1 打出点数最大的双牌
    def way1(self,start_result, end_result, table_poker):
        result = []
        shuangpai_list = []
        for v in start_result:
            if v[0] == v[1]:
                shuangpai_list.append([v, 0])
        for v in end_result:
            if v[0] == v[1]:
                shuangpai_list.append([v, 1])
        if len(shuangpai_list) > 0:
            max_dianshu = max([v[0][0] for v in shuangpai_list])
            for v in shuangpai_list:
                if max_dianshu == v[0][0]:
                    #print(self.name + "选了双牌 " + str(max_dianshu) + " 双牌总共有 " + str(shuangpai_list))
                    return v
        return result

        # 根据桌面上已经打出的牌，判断玩家手上胜的牌。 打的牌能让其它凑牌的概率最小

    def way2(self, start_result, end_result, table_poker, player_list):
        total_result = start_result + end_result
        min = 1000
        for v in total_result:
            match_num = 0
            for left_poker in table_poker.getPlayersPoker(self):
                if v[0] == left_poker[0] or v[0] == left_poker[1]:
                    match_num = match_num + 1
                if v[1] == left_poker[0] or v[1] == left_poker[1]:
                    match_num = match_num + 1
            if match_num < min:
                min = match_num

        for index, v in enumerate(total_result):
            match_num = 0
            for left_poker in table_poker.getPlayersPoker(self):
                if v[0] == left_poker[0] or v[0] == left_poker[1]:
                    match_num = match_num + 1
                if v[1] == left_poker[0] or v[1] == left_poker[1]:
                    match_num = match_num + 1
            if match_num == min:
                # print("excellent!!!!!!!!!    min:"+str(min))
                if index < len(start_result):
                    return [v, 0]
                else:
                    return [v, 1]

        return []
    # 打出点数最大的牌
    def way3(self, start_result, end_result, table_poker):

        list1 = [v[0] + v[1] for v in start_result]
        list2 = [v[0] + v[1] for v in end_result]
        max_points1 = 0
        max_points2 = 0
        if len(list1) > 0:
            max_points1 = max(list1)
        if len(list2) > 0:
            max_points2 = max(list2)
        if max_points1 > max_points2:
            for v in start_result:
                if v[0] + v[1] == max_points1:
                    return [v, 0]
        else:
            for v in end_result:
                if v[0] + v[1] == max_points2:
                    return [v, 1]
        return []

    # 让自己剩余的牌覆盖最多的点数
    def way4(self, start_result, end_result, table_poker):
        total_result = start_result + end_result
        max = 0
        for v1 in total_result:
            mid_result = [0, 0, 0, 0, 0, 0, 0]
            for v2 in self.poker_list:
                if v1 == v2:
                    continue
                mid_result[v2[0]] = 1
                mid_result[v2[1]] = 1
            sum_res = sum(mid_result)
            if sum_res > max:
                max = sum_res
        if max == 0:
            return []

        for index, v1 in enumerate(total_result):
            mid_result = [0, 0, 0, 0, 0, 0, 0]
            for v2 in self.poker_list:
                if v1 == v2:
                    continue
                mid_result[v2[0]] = 1
                mid_result[v2[1]] = 1
            sum_res = sum(mid_result)
            if sum_res == max:
                # print("max  "+str(max))
                if index < len(start_result):
                    return [v1, 0]
                else:
                    return [v1, 1]

        return []


    # 根据已经出牌的情况，打出让对手配不了的牌
    def way5(self, start_result, end_result, table_poker, player_list):
        total_result = start_result + end_result
        max = 0
        for v in total_result:
            pass_num = 0
            for player in player_list:
                if player.get_name() == self.name:
                    continue
                if v[0] in player.get_pass_poker():
                    pass_num = pass_num + 1
                if v[1] in player.get_pass_poker():
                    pass_num = pass_num + 1
            if pass_num > max:
                max = pass_num
        # 配不上，或者只配了一个，那就算了
        if max == 0 or max == 1:
            #print("sorry, way4 not implemented")
            return []
        for index, v in enumerate(total_result):
            pass_num = 0
            for player in player_list:
                if player.get_name() == self.name:
                    continue
                if v[0] in player.get_pass_poker():
                    pass_num = pass_num + 1
                if v[1] in player.get_pass_poker():
                    pass_num = pass_num + 1
            if pass_num == max:
                #print("good!!!!!!!!!    max:"+str(max))
                if index < len(start_result):
                    return [v, 0]
                else:
                    return [v, 1]
        return []






    # top10 打出让弃牌首端和尾端的牌保持不变
    def way10(self, start_result, end_result, table_poker):
        if table_poker.has_two_poker():
            a1 = table_poker.getStartPoker()[0]
            a2 = table_poker.getStartPoker()[1]
            b1 = table_poker.getEndPoker()[0]
            b2 = table_poker.getEndPoker()[1]
            for v in start_result:
                if a1 == v[0] and b1 == v[1] and v[0] != v[1]:
                    return [v, 0]
                elif a1 == v[0] and b2 == v[1] and v[0] != v[1]:
                    return [v, 0]
                elif a2 == v[0] and b2 == v[1] and v[0] != v[1]:
                    return [v, 0]
                elif a2 == v[0] and b1 == v[1] and v[0] != v[1]:
                    return [v, 0]
            for v in end_result:
                if a1 == v[0] and b1 == v[1] and v[0] != v[1]:
                    return [v, 1]
                elif a1 == v[0] and b2 == v[1] and v[0] != v[1]:
                    return [v, 1]
                elif a2 == v[0] and b2 == v[1] and v[0] != v[1]:
                    return [v, 1]
                elif a2 == v[0] and b1 == v[1] and v[0] != v[1]:
                    return [v, 1]
        return []
    def choose_poker_with_state(self,start_result, end_result, table_poker, player_list):
        result = []

        # top1 打出点数最大的双牌  126029
        result = self.way1(start_result, end_result, table_poker)
        if len(result) > 0:
            return result

        # top2 打出让对手配不了的牌,根据对手还剩的牌（自己手上的牌，加上桌上打出的牌来推测） 122675
        result = self.way2(start_result, end_result, table_poker, player_list)
        if len(result) > 0:
            return result

        # top3 打出点数最大的牌 105887
        result = self.way3(start_result, end_result, table_poker)
        if len(result) > 0:
            return result

        # top4 打出的牌让手上的牌尽可能包含更多样的点数（覆盖1-6的点数，越多越好，最大为7） 103947
        result = self.way4(start_result, end_result, table_poker)
        if len(result) > 0:
            return result

        # top5 打出让对手配不了的牌（根据对手报pass的牌 ）101073
        result = self.way5(start_result, end_result, table_poker, player_list)
        if len(result) > 0:
            return result




        for v in start_result:
            result = [v, 0]
            return result
        for v in end_result:
            result = [v, 1]
            return result
        return result
class TablePoker:
    def __init__(self):
        self.pokerlist = []

    def getPokerList(self):
        return self.pokerlist

    def getPlayersPoker(self, player):
        players_pokerlist = []
        for v in all_poker_list:
            if v not in self.pokerlist and v not in player.get_poker_list():
                players_pokerlist.append(v)
        return players_pokerlist
    def getStartPoker(self):
        if len(self.pokerlist):
            return self.pokerlist[0]
        else:
            return []
    def getEndPoker(self):
        if len(self.pokerlist):
            return self.pokerlist[-1]
        else:
            return []

    def getPassPoker(self):
        if len(self.pokerlist) < 1:
            return []
        return [self.pokerlist[0][0], self.pokerlist[0][1], self.pokerlist[-1][0], self.pokerlist[-1][1]]

    def chupai(self, poker, start_or_end):
        if start_or_end == 0:
            self.pokerlist.insert(0, poker)
        else:
            self.pokerlist.append(poker)

    def has_two_poker(self):
        if len(self.pokerlist) > 1:
            return True
        else:
            return  False



def try_one_time():
    np.random.shuffle(all_poker_list)
    player_1 = Player("A", all_poker_list[0:7])
    player_2 = Player("B", all_poker_list[7:14])
    player_3 = CleverPlayer("C", all_poker_list[14:21])
    # player_3 = Player("C", all_poker_list[14:21])
    player_4 = Player("D", all_poker_list[21:28])
    table_poker = TablePoker()
    player_list = [player_1, player_2, player_3, player_4]
    np.random.shuffle(player_list)
    for i in range(15):
        #print("*****第{0}轮开始*******".format(i + 1))
        #print(table_poker.pokerlist)
        #player_1.print_left_poker()
        #player_2.print_left_poker()
        #player_3.print_left_poker()
        #player_4.print_left_poker()

        res1 = player_list[0].chupai(table_poker, player_list)
        if res1 == 0:
            player_list[0].add_pass_poker(table_poker.getStartPoker())
        if player_list[0].has_no_poker():
            return player_list[0].get_win_result()


        res2 = player_list[1].chupai(table_poker, player_list)
        if res2 == 0:
            player_list[1].add_pass_poker(table_poker.getStartPoker())
        if player_list[1].has_no_poker():
            return player_list[1].get_win_result()


        res3 = player_list[2].chupai(table_poker, player_list)
        if res3 == 0:
            player_list[2].add_pass_poker(table_poker.getStartPoker())
        if player_list[2].has_no_poker():
            return player_list[2].get_win_result()


        res4 = player_list[3].chupai(table_poker, player_list)
        if res4 == 0:
            player_list[3].add_pass_poker(table_poker.getStartPoker())
        if player_list[3].has_no_poker():
            return player_list[3].get_win_result()


        if res1 + res2 + res3 + res4 == 0:
            #print("*******dead end**********")
            break
    min_fen = min(player_1.suan_fen(), player_2.suan_fen(), player_3.suan_fen(), player_4.suan_fen())
    if player_1.suan_fen() == min_fen:
        return [1, 0, 0, 0]
    elif player_2.suan_fen() == min_fen:
        return [0, 1, 0, 0]
    elif player_3.suan_fen() == min_fen:
        return [0, 0, 1, 0]
    else:
        return [0, 0, 0, 1]



if __name__ == '__main__':
    res = [0,0,0,0]
    for i in range(1000):
        r = try_one_time()
        res = [m + n for m,n in zip(res, r)]
    print(res)



