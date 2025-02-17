import matplotlib.pyplot as plt
from io import BytesIO


async def pie_hours_extra(vals, labels):
    indexes_to_remove = []
    for i in range(len(vals)):
        if labels[i] != 'Да' and labels[i] != "Нет":
            indexes_to_remove.append(i)
    final_vals = [item for idx, item in enumerate(vals) if idx not in indexes_to_remove]
    final_labels = [item for idx, item in enumerate(labels) if idx not in indexes_to_remove]    
    fig, ax = plt.subplots()
    def func(pct, s, val):
        return f"{val} {s} ({pct:.1f}%)"
    colors = ['skyblue', 'cornflowerblue']
    wedges, texts, autotexts = ax.pie(
        final_vals, 
        labels=final_labels, 
        autopct=lambda pct: func(pct, "часов\n", int(final_vals[int(pct / 100 * len(final_vals))])),
        startangle=90,
        colors=colors,
        )
    ax.axis('equal')
    plt.title(
    label="Соотношение часов дополнительных работ и основных", 
    fontdict={"fontsize":14},
    pad=20)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf


async def hist_hours_by_objects(vals, labels):
    indexes_to_remove = []
    for i in range(len(vals)):
        if vals[i] is None:
            indexes_to_remove.append(i)
    final_vals = [item for idx, item in enumerate(vals) if idx not in indexes_to_remove]
    final_labels = [item for idx, item in enumerate(labels) if idx not in indexes_to_remove]    
    fig, ax = plt.subplots()
    colors = ['skyblue', 'steelblue', 'deepskyblue', 'powderblue',  'cornflowerblue', 'lightskyblue', 'dodgerblue', 'lightcyan']
    bar_container = ax.bar(final_labels, final_vals, color=colors)
    ax.set(ylabel='Часы', title='Распределение человекочасов по объектам')
    ax.bar_label(bar_container, fmt='{:,.0f}')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf
