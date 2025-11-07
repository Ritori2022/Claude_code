#!/usr/bin/env python3
"""
快速演示脚本 - 观看AI们玩狼人杀
"""

from werewolf import WerewolfGame, create_agent_personalities


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║           🌙 AI多人格狼人杀游戏系统 🐺                   ║
    ║                                                          ║
    ║        6位性格迥异的AI将展开激烈的推理对决!              ║
    ║                                                          ║
    ║        它们会撒谎,会推理,会互相怀疑...                   ║
    ║        谁能笑到最后?                                     ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    print("\n🎭 参赛选手介绍:\n")
    personalities = create_agent_personalities()

    for i, p in enumerate(personalities):
        print(f"  {i}. {p.traits['intro']}")

    print("\n" + "="*60)
    print("游戏即将开始...")
    print("="*60)

    # 创建并运行游戏
    game = WerewolfGame(personalities)
    game.run()

    print("\n\n💭 思考一下:")
    print("  - 哪个AI的推理最合理?")
    print("  - 狼人的伪装是否成功?")
    print("  - 如果让这些AI学习和进化,它们会变得更聪明吗?")
    print("\n✨ 感谢观看! 可以再次运行查看不同的游戏进程~\n")


if __name__ == "__main__":
    main()
