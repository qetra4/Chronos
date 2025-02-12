import matplotlib.pyplot as plt

async def pie_hours_extra(vals, labels):
    fig, ax = plt.subplots()
    total = sum(vals)
    percentages = [(val / total) * 100 for val in vals]

    def func(pct, s, val):
        return f"{val} {s} ({pct:.1f}%)"
    
    wedges, texts, autotexts = ax.pie(
        vals, 
        labels=labels, 
        autopct=lambda pct: func(pct, "часов\n", int(vals[int(pct / 100 * len(vals))])),
        startangle=90
    )
    
    for text in autotexts:
        text.set_color('white')
    ax.axis('equal')
    plt.show()


async def hist_hours_by_objects(vals, labels):
    fig, ax = plt.subplots()
    bar_container = ax.bar(labels, vals)
    ax.set(ylabel='Часы', title='Распределение человекочасов по объектам')
    ax.bar_label(bar_container, fmt='{:,.0f}')
    plt.tight_layout()
    plt.show()