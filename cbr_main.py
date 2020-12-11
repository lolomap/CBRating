# coding=utf-8
import data_manage
import vk_manage

group_ids = data_manage.read_group_ids()

groups_info = vk_manage.get_groups_info(group_ids)
group_names = {}
for info in groups_info:
    group_names[info['id']] = info['name']

last = data_manage.read_last(groups_info)

post_text = data_manage.write_data(groups_info, last)

full_plot_data, plot_data = data_manage.generate_plot_data()
data_manage.generate_plot(plot_data, group_names)
data_manage.generate_inflow_diagram(full_plot_data)
'''
groups_k = {}
for info in groups_info:
    days = len(list(plot_data.values())[0])
    posts_info = vk_manage.get_group_posts_count(-info['id'], days)
    posts = posts_info['count']
    likes = posts_info['likes']
    comments = posts_info['comments']
    group_k = data_manage.k_calculate(days, posts, likes, comments, info['members_count'])
    groups_k[info['id']] = group_k

data_manage.generate_k_plot(group_names, groups_k)
'''
plot_photo = vk_manage.upload_photo('plot')
inf_photo = vk_manage.upload_photo('inf')
# k_photo = vk_manage.upload_photo('k')

vk_manage.post(post_text, [plot_photo, inf_photo])
