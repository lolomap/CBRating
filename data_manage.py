# coding=utf-8
from settings import DIRECTORIES, DEBUG
import matplotlib.pyplot as plt


def generate_plot_data():
    long_data = open(DIRECTORIES['long_data'], 'r')
    week_data = []
    for section in long_data.read().split('**SECTION**'):
        if section == '':
            continue
        group = {}
        for line in section.split('\n'):
            if line == '':
                continue
            pair = line.split('=')
            if pair[1] == 'None':
                group[int(pair[0])] = None
            else:
                group[int(pair[0])] = int(pair[1])
        if group != {}:
            week_data.append(group)

    plot_data = {}
    for day in week_data:
        for item in day.items():
            if not plot_data.keys().__contains__(item[0]):
                plot_data[item[0]] = []
            plot_data[item[0]].append(item[1])
    full_plot_data = plot_data.copy()
    list_plot_data = list(plot_data.items())
    list_plot_data.sort(key=lambda x: x[1][-1], reverse=True)
    plot_data.clear()
    try:
        for j in range(0, 5):
            plot_data[list_plot_data[j][0]] = list_plot_data[j][1]
    except IndexError:
        pass
    return full_plot_data, plot_data


def generate_plot(plot_data, group_names):
    fig, pl = plt.subplots()
    plt.title('График роста подписчиков', fontweight='bold')
    plt.xlabel('Дни')
    plt.ylabel('Подписчики в день')
    for item in plot_data.items():
        try:
            name = group_names[item[0]]
            pl.plot(item[1], label=name)
        except KeyError:
            pass

    pl.legend(title='Самые быстрорастущие\nгруппы за последние сутки', bbox_to_anchor=(1.05, 1), ncol=1)
    pl.minorticks_on()
    pl.grid(which='major')
    pl.grid(which='minor', linestyle=':')
    fig.savefig(DIRECTORIES['photo'], bbox_inches='tight')


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct


def generate_inflow_diagram(f_pd):
    inf = 0
    outf = 0
    for item in f_pd.items():
        for num in item[1]:
            if num is None:
                continue
            if num > 0:
                inf = inf + num
            else:
                outf = outf + num
    fig, ax = plt.subplots()
    plt.title('Динамика подписчиков КБ групп', fontweight='bold')
    values = [inf, abs(outf)]
    ax.pie(values, labels=['Приток', 'Отток'], autopct=make_autopct(values))
    ax.axis('equal')
    fig.savefig(DIRECTORIES['inf_photo'], bbox_inches='tight')


def read_group_ids():
    group_ids = []
    for line in open(DIRECTORIES['list'], 'r'):
        if line[:3] == 'id:':
            i = int(line[3:])
            group_ids.append(i)
        else:
            group_ids.append(line)
    return group_ids


def write_data(groups_info, last):
    data = open(DIRECTORIES['data'], 'w')
    long_data = open(DIRECTORIES['long_data'], 'a')
    post_text = 'Актуальный рейтинг групп:\n\n'
    num = 0
    long_data.write('**SECTION**\n')
    for group in groups_info:
        num = num + 1
        symbol = ''
        try:
            d = group['members_count'] - last[group['id']]
        except KeyError:
            d = 0
        if d > 0:
            post_text = post_text + '📈 '
            symbol = '+'
        elif d < 0:
            post_text = post_text + '📉 '
        else:
            post_text = post_text + '⏸ '
        post_text = post_text + str(num) + '. ['
        if not DEBUG:
            post_text = post_text + 'club'
        post_text = post_text + str(group['id']) + '|' + group['name'] + ']: ' + str(group['members_count']) \
            + ' (' + symbol + str(d) + ')\n'
        data.write(str(group['id']) + '=' + str(group['members_count']) + '\n')
        long_data.write(str(group['id']) + '=' + str(d) + '\n')
    long_data.close()
    return post_text


def read_last(groups_info):
    data = open(DIRECTORIES['data'], 'r')
    groups_info.sort(key=lambda x: x['members_count'], reverse=True)
    last = {}
    for line in data:
        pair = line.split('=')
        pair[1] = pair[1][:-1]
        last[int(pair[0])] = int(pair[1])
    data.close()
    return last


def k_calculate(days, posts, likes, comments, subs):
    k_adm = posts / days
    k_aud = (likes + comments)/days/subs
    return round((k_adm + k_aud)*10, 2)


def generate_k_plot(group_names, groups_k):
    fig, ax = plt.subplots()
    plt.title('Коэффиценты активности групп', fontweight='bold')
    names = []
    for item in groups_k.items():
        names.append(group_names[item[0]])
    x = range(0, len(list(groups_k.items())))

    ax.barh(x, groups_k.values())
    ax.set_yticks(x)
    ax.set_yticklabels(names)
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=':')
    fig.savefig(DIRECTORIES['k_photo'], bbox_inches='tight')
    return
