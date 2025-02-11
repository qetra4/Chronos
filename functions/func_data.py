import matplotlib.pyplot as plt

async def pie_hours_extra(vals, labels):
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels)
    ax.axis("equal")
    plt.show()

async def hist_hours_by_objects(vals, labels):
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels)
    ax.axis("equal")
    plt.show()
    pass
