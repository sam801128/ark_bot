import random
import discord
from discord.ext import commands
import json

with open('setting.json', 'r',encoding='utf8') as jfile:
  jdata = json.load(jfile)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix ="/",intents = intents)


@bot.command()
async def group(ctx, num_groups: int, *, conflicts: str = None):
    # 指定身分組
    role_name = "小丑"
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"找不到角色 {role_name}。")
        return

    members_with_role = [member for member in role.members]

    if len(members_with_role) < num_groups:
        await ctx.send("成員數量不足，無法分成這麼多隊。")
        return

    # 解析不能同隊的成員
    conflict_pairs = {}
    if conflicts:
        conflict_list = conflicts.split(',')
        for pair in conflict_list:
            members = pair.split('&')
            if len(members) == 2:
                conflict_pairs[members[0].strip()] = members[1].strip()
                conflict_pairs[members[1].strip()] = members[0].strip()  # 確保雙向衝突

    # 隨機分組
    random.shuffle(members_with_role)

    groups = [[] for _ in range(num_groups)]

    # 進行分組，確保不會有空組
    for i, member in enumerate(members_with_role):
        placed = False
        for _ in range(num_groups):  # 確保遍歷所有組
            group_index = (i % num_groups)  # 根據索引進行分配
            group = groups[group_index]

            # 檢查這組是否有任何衝突的成員
            if not any(conflict_pairs.get(member.display_name) == other_member.display_name for other_member in group):
                group.append(member)
                placed = True
                break
            
            i += 1  # 遍歷下一個成員

        if not placed:
            await ctx.send("無法將所有成員分組，因為存在衝突。")
            return

    # 確保沒有空組
    for group in groups:
        if not group:
            await ctx.send("無法將所有成員分組，因為存在衝突。")
            return

    response = "分組結果：\n"
    for i, group in enumerate(groups):
        member_names = ", ".join(member.display_name for member in group)
        response += f"組 {i + 1}: {member_names}\n"

    await ctx.send(response)

bot.run(jdata['TOKEN'])