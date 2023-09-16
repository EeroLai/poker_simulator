import random

# 初始化牌堆
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

# 洗牌
random.shuffle(deck)

# 發牌给8名玩家
players = [[] for _ in range(8)]

for _ in range(2):
    for i in range(8):
        players[i].append(deck.pop())


# 初始化牌池
community_cards = []

# 牌池（公共牌池）
for _ in range(5):
    community_cards.append(deck.pop())

for i, player_hand in enumerate(players):
    print(f"玩家{i+1}的手牌:", player_hand)

print("牌池（公共牌池）:", community_cards)

# 牌型判定
def evaluate_hand(hand):
    # 分離花色和點數
    ranks = [card['rank'] for card in hand]
    suits = [card['suit'] for card in hand]
    
    # 統計點數出現的次數
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    sorted_ranks = sorted(set(ranks), key=lambda x: ranks.index(x))

    # 判斷是否有同花
    if len(set(suits)) == 1:
        # 判斷是否有順子
        if len(sorted_ranks) == 5 and is_straight(hand):
            return "同花順", max(sorted_ranks)
        else:
            return "同花", max(sorted_ranks)

    
    # 判斷是否有四條、葫蘆、三條、兩對或一對
    rank_values = list(rank_counts.values())
    if 4 in rank_values:
        return "四條", ranks[rank_values.index(4)]
    if 3 in rank_values and 2 in rank_values:
        three_rank_index = rank_values.index(3)
        two_rank_index = None
        
        # 查找第二個值為2的元素的索引
        for i in range(three_rank_index + 1, len(rank_values)):
            if rank_values[i] == 2:
                two_rank_index = i
                break
        
        if two_rank_index is not None:
            three_rank = ranks[three_rank_index]
            two_rank = ranks[two_rank_index]
            return "葫蘆", (three_rank, two_rank)
    if 3 in rank_values:
        return "三條", ranks[rank_values.index(3)]
    if rank_values.count(2) == 2:
        pair_ranks = []
        for _ in range(2):
            pair_ranks.append(ranks[rank_values.index(2)])
            rank_values[rank_values.index(2)] = 0  # 防止重複選取相同點數的對子
        return "兩對", tuple(sorted(pair_ranks, reverse=True))
    if 2 in rank_values:
        pair_rank = ranks[rank_values.index(2)]
        return "一對", pair_rank
    
    # 判斷是否有順子
    if is_straight(hand):
        return "順子", max(sorted_ranks)
    
    # 否則是高牌
    return "高牌", max(rank_counts)

# 比較玩家手牌並找出獲勝者
best_hand = ("高牌", 0)
winning_players = []

def is_straight(hand):
    # 定義Mapping表
    value_map = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': [1, 14] # A可以是1或14
    }

    # 將手牌中的牌值對應為數字
    values = [value_map[card['rank']] for card in hand]

    # 將A按可能的值分割成兩張牌
    for i, value in enumerate(values):
        if isinstance(value, list):
            # 如果A有兩種可能的值，我們可以嘗試兩種情況
            values[i] = value[1]
            new_values = values.copy()
            new_values[i] = value[0]
            # 檢查兩種情況中是否有順子
            if is_straight_helper(new_values) or is_straight_helper(values):
                return True

    # 如果沒有A，或者兩種情況都不是順子，則只檢查一次
    return is_straight_helper(values)

def is_straight_helper(values):
    # 排序
    values.sort()

    # 檢查是否連續
    for i in range(len(values) - 1):
        if values[i + 1] - values[i] != 1:
            return False

    return True

# for i, player_hand in enumerate(players):
#     hand_type, hand_rank = evaluate_hand( [
#     {'rank': '3', 'suit': '♣'},
#     {'rank': 'A', 'suit': '♥'},
#     {'rank': '2', 'suit': '♦'},
#     {'rank': '4', 'suit': '♥'},
#     {'rank': '5', 'suit': '♠'}
# ])
    
for i, player_hand in enumerate(players):
    hand_type, hand_rank = evaluate_hand( [
    {'rank': 'K', 'suit': '♣'},
    {'rank': 'A', 'suit': '♥'},
    {'rank': 'Q', 'suit': '♦'},
    {'rank': 'J', 'suit': '♥'},
    {'rank': '10', 'suit': '♠'}
])
    print(hand_type, hand_rank)
    # if hand_rank > best_hand[1]:
    #     best_hand = (hand_type, hand_rank)
    #     winning_players = [i + 1]
    # elif hand_rank == best_hand[1]:
    #     winning_players.append(i + 1)

# # 誰獲勝
# if len(winning_players) == 1:
#     print(f"玩家{winning_players[0]}獲勝！")
# else:
#     print("平局！獲勝玩家:", winning_players)