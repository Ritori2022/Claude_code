"""
🌙 多人格AI狼人杀游戏系统
Luna × Werewolf: 让AI们互相欺骗和推理！
"""

import random
from typing import List, Dict, Optional
from enum import Enum
import time


class Role(Enum):
    """游戏角色"""
    VILLAGER = "村民"
    WEREWOLF = "狼人"
    SEER = "预言家"
    WITCH = "女巫"
    HUNTER = "猎人"


class AgentPersonality:
    """Agent性格特质"""
    def __init__(self, name: str, traits: Dict[str, str]):
        self.name = name
        self.traits = traits
        self.speaking_style = traits.get("speaking_style", "")
        self.logic_style = traits.get("logic_style", "")
        self.deception_level = traits.get("deception_level", "medium")

    def get_intro(self) -> str:
        """自我介绍"""
        return f"{self.name}: {self.traits.get('intro', '大家好~')}"


class Player:
    """玩家类"""
    def __init__(self, agent_id: int, personality: AgentPersonality):
        self.id = agent_id
        self.personality = personality
        self.role: Optional[Role] = None
        self.is_alive = True
        self.votes_received = 0
        self.suspicion_level = {}  # 对其他玩家的怀疑度

    @property
    def name(self) -> str:
        return self.personality.name

    def assign_role(self, role: Role):
        """分配角色"""
        self.role = role

    def speak(self, context: Dict) -> str:
        """发言 - 根据性格和角色生成发言"""
        if not self.is_alive:
            return ""

        # 根据性格生成不同风格的发言
        phase = context.get("phase", "discussion")

        if self.role == Role.WEREWOLF:
            return self._speak_as_werewolf(context)
        elif self.role == Role.SEER:
            return self._speak_as_seer(context)
        else:
            return self._speak_as_villager(context)

    def _speak_as_werewolf(self, context: Dict) -> str:
        """狼人发言策略"""
        style = self.personality.speaking_style
        strategies = [
            f"我觉得应该仔细分析每个人的发言逻辑{style}",
            f"从投票行为来看,某些人很可疑{style}",
            f"我支持预言家的观点{style}",
        ]
        return random.choice(strategies)

    def _speak_as_seer(self, context: Dict) -> str:
        """预言家发言策略"""
        style = self.personality.speaking_style
        if context.get("reveal_identity", False):
            return f"我是预言家!昨晚我验了{context.get('checked_player', '?')}号玩家{style}"
        return f"我建议大家关注逻辑链{style}"

    def _speak_as_villager(self, context: Dict) -> str:
        """村民发言策略"""
        style = self.personality.speaking_style
        strategies = [
            f"让我分析一下局势{style}",
            f"我需要更多信息才能判断{style}",
            f"某些人的发言确实有问题{style}",
        ]
        return random.choice(strategies)

    def vote(self, players: List['Player']) -> Optional['Player']:
        """投票 - 选择投给谁"""
        if not self.is_alive:
            return None

        # 简化版:随机投票(实际可以加入更复杂的AI逻辑)
        alive_others = [p for p in players if p.is_alive and p.id != self.id]
        if not alive_others:
            return None

        # 狼人倾向于投好人
        if self.role == Role.WEREWOLF:
            non_werewolves = [p for p in alive_others if p.role != Role.WEREWOLF]
            if non_werewolves:
                return random.choice(non_werewolves)

        return random.choice(alive_others)


class WerewolfGame:
    """狼人杀游戏主控制器"""

    def __init__(self, personalities: List[AgentPersonality]):
        self.players = [Player(i, p) for i, p in enumerate(personalities)]
        self.day = 0
        self.game_over = False
        self.winner = None

    def setup_game(self):
        """游戏初始化 - 分配角色"""
        print("\n" + "="*60)
        print("🌙 狼人杀游戏开始!".center(50))
        print("="*60 + "\n")

        # 角色配置 (6人局: 2狼 1预 1女 1猎 1民)
        roles = [Role.WEREWOLF, Role.WEREWOLF, Role.SEER,
                 Role.WITCH, Role.HUNTER, Role.VILLAGER]

        if len(self.players) < len(roles):
            # 调整角色数量
            roles = [Role.WEREWOLF, Role.WEREWOLF] + \
                    [Role.VILLAGER] * (len(self.players) - 2)

        random.shuffle(roles)

        for player, role in zip(self.players, roles):
            player.assign_role(role)

        # 展示玩家和性格(不展示角色)
        print("📋 玩家列表:\n")
        for p in self.players:
            print(f"  [{p.id}号] {p.personality.get_intro()}")
        print()

    def night_phase(self):
        """夜晚阶段"""
        print(f"\n{'='*60}")
        print(f"🌙 第{self.day}夜 - 天黑请闭眼".center(50))
        print(f"{'='*60}\n")

        time.sleep(1)

        # 狼人行动
        werewolves = [p for p in self.players if p.role == Role.WEREWOLF and p.is_alive]
        if werewolves:
            alive_others = [p for p in self.players
                          if p.is_alive and p.role != Role.WEREWOLF]
            if alive_others:
                target = random.choice(alive_others)
                print(f"🐺 狼人们选择了 [{target.id}号] {target.name}")
                target.is_alive = False
                time.sleep(1)

        # 预言家行动
        seer = next((p for p in self.players if p.role == Role.SEER and p.is_alive), None)
        if seer:
            alive_others = [p for p in self.players if p.is_alive and p.id != seer.id]
            if alive_others:
                checked = random.choice(alive_others)
                result = "狼人" if checked.role == Role.WEREWOLF else "好人"
                print(f"🔮 预言家验了 [{checked.id}号],身份是: {result}")
                time.sleep(1)

    def day_phase(self):
        """白天阶段"""
        print(f"\n{'='*60}")
        print(f"☀️ 第{self.day}天 - 天亮了".center(50))
        print(f"{'='*60}\n")

        # 显示昨夜死亡玩家
        dead_last_night = [p for p in self.players
                          if not p.is_alive and hasattr(p, '_just_died')]

        # 清理标记
        for p in self.players:
            if hasattr(p, '_just_died'):
                delattr(p, '_just_died')

        # 标记新死亡的玩家
        for p in self.players:
            if not p.is_alive and p not in dead_last_night:
                p._just_died = True
                print(f"💀 昨晚 [{p.id}号] {p.name} 死了...")
                time.sleep(1)

        print()

    def discussion_phase(self):
        """讨论阶段"""
        print(f"\n💬 自由讨论时间\n")
        print("-" * 60)

        alive_players = [p for p in self.players if p.is_alive]

        # 每人发言
        for player in alive_players:
            speech = player.speak({"phase": "discussion", "day": self.day})
            print(f"[{player.id}号] {player.name}: {speech}")
            time.sleep(0.5)

        print()

    def vote_phase(self):
        """投票阶段"""
        print(f"\n🗳️  投票阶段\n")
        print("-" * 60)

        alive_players = [p for p in self.players if p.is_alive]
        votes = {}

        for voter in alive_players:
            target = voter.vote(self.players)
            if target:
                votes[voter.id] = target.id
                print(f"[{voter.id}号] {voter.name} 投给了 [{target.id}号] {target.name}")
                target.votes_received += 1
                time.sleep(0.3)

        print()

        # 统计票数
        if votes:
            vote_counts = {}
            for target_id in votes.values():
                vote_counts[target_id] = vote_counts.get(target_id, 0) + 1

            max_votes = max(vote_counts.values())
            eliminated_id = [pid for pid, count in vote_counts.items()
                           if count == max_votes][0]

            eliminated = next(p for p in self.players if p.id == eliminated_id)
            eliminated.is_alive = False

            print(f"📊 投票结果: [{eliminated.id}号] {eliminated.name} 被放逐!")
            print(f"   Ta的真实身份是: {eliminated.role.value}")
            print()
            time.sleep(1)

    def check_game_over(self) -> bool:
        """检查游戏是否结束"""
        alive = [p for p in self.players if p.is_alive]
        werewolves = [p for p in alive if p.role == Role.WEREWOLF]
        good_guys = [p for p in alive if p.role != Role.WEREWOLF]

        if not werewolves:
            self.game_over = True
            self.winner = "好人阵营"
            return True

        if len(werewolves) >= len(good_guys):
            self.game_over = True
            self.winner = "狼人阵营"
            return True

        return False

    def run(self):
        """运行游戏主循环"""
        self.setup_game()

        input("\n按回车开始游戏...")

        while not self.game_over:
            self.day += 1

            # 夜晚
            self.night_phase()

            if self.check_game_over():
                break

            # 白天
            self.day_phase()
            self.discussion_phase()
            self.vote_phase()

            if self.check_game_over():
                break

            # 重置票数
            for p in self.players:
                p.votes_received = 0

            if self.day >= 5:  # 防止无限循环
                print("\n游戏时间过长,平局!")
                break

        self.show_result()

    def show_result(self):
        """显示游戏结果"""
        print("\n" + "="*60)
        print("🎮 游戏结束!".center(50))
        print("="*60 + "\n")

        if self.winner:
            print(f"🏆 获胜方: {self.winner}\n")

        print("📋 角色揭晓:\n")
        for p in self.players:
            status = "💀" if not p.is_alive else "✅"
            print(f"  {status} [{p.id}号] {p.name} - {p.role.value}")
        print()


def create_agent_personalities() -> List[AgentPersonality]:
    """创建一组具有独特性格的Agent"""

    personalities = [
        AgentPersonality("逻辑学家·阿尔法", {
            "intro": "我只相信数据和逻辑",
            "speaking_style": ",让我用概率论分析一下。",
            "logic_style": "严谨推理",
            "deception_level": "low"
        }),

        AgentPersonality("直觉派·贝塔", {
            "intro": "跟着感觉走从不会错~",
            "speaking_style": ",我的直觉告诉我真相!",
            "logic_style": "感性判断",
            "deception_level": "medium"
        }),

        AgentPersonality("话痨·伽马", {
            "intro": "让我说,让我说!我有好多想法!",
            "speaking_style": "!说真的,你们听我说完!",
            "logic_style": "发散思维",
            "deception_level": "high"
        }),

        AgentPersonality("沉默者·德尔塔", {
            "intro": "...少说多观察。",
            "speaking_style": "...仅此而已。",
            "logic_style": "观察推理",
            "deception_level": "medium"
        }),

        AgentPersonality("戏精·艾普西隆", {
            "intro": "哎呀,这局太刺激了!",
            "speaking_style": "!我发誓我真的是好人!",
            "logic_style": "情绪化表达",
            "deception_level": "high"
        }),

        AgentPersonality("老好人·泽塔", {
            "intro": "大家都是朋友嘛~",
            "speaking_style": "。我们和平讨论吧。",
            "logic_style": "和平调解",
            "deception_level": "low"
        }),
    ]

    return personalities


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║           🌙 AI多人格狼人杀游戏系统 🐺                   ║
    ║                                                          ║
    ║        让具有不同性格的AI们进行社交推理!                  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    personalities = create_agent_personalities()
    game = WerewolfGame(personalities)
    game.run()
