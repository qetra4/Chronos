import matplotlib.pyplot as plt


async def pie_hours_extra(vals, labels):
    indexes_to_remove = []
    for i in range(len(vals)):
        if labels[i] != 'Да' and labels[i] != "Нет":
            indexes_to_remove.append(i)
    print(indexes_to_remove)
    final_vals = [item for idx, item in enumerate(vals) if idx not in indexes_to_remove]
    final_labels = [item for idx, item in enumerate(labels) if idx not in indexes_to_remove]    
    fig, ax = plt.subplots()
    total = sum(final_vals)
    percentages = [(val / total) * 100 for val in final_vals]
    def func(pct, s, val):
        return f"{val} {s} ({pct:.1f}%)"
    wedges, texts, autotexts = ax.pie(
        final_vals, 
        labels=final_labels, 
        autopct=lambda pct: func(pct, "часов\n", int(final_vals[int(pct / 100 * len(final_vals))])),
        startangle=90
        )
    for text in autotexts:
        text.set_color('white')
    ax.axis('equal')
    plt.show()


async def hist_hours_by_objects(vals, labels):
    indexes_to_remove = []
    for i in range(len(vals)):
        if vals[i] is None:
            indexes_to_remove.append(i)
    final_vals = [item for idx, item in enumerate(vals) if idx not in indexes_to_remove]
    final_labels = [item for idx, item in enumerate(labels) if idx not in indexes_to_remove]    
    fig, ax = plt.subplots()
    bar_container = ax.bar(final_labels, final_vals)
    ax.set(ylabel='Часы', title='Распределение человекочасов по объектам')
    ax.bar_label(bar_container, fmt='{:,.0f}')
    plt.tight_layout()
    plt.show()
