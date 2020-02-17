import datetime
from uuid import uuid4

from matplotlib import pyplot as plt, dates as mdates

from models import Rate
from api import ExchangeratesAPILatest, ExchangeratesAPIHistory


def get_or_create_actual_rate_instance():
    last_record = Rate.select().order_by(Rate.id.desc()).first()
    if not last_record or (datetime.datetime.now() - last_record.created_date) > datetime.timedelta(minutes=10):
        is_success, message, objects = ExchangeratesAPILatest()()
        if is_success:
            last_record = Rate.create(raw_rates=objects["rates"], created_date=objects["date"])
        else:
            raise Exception(message)
    return last_record


def generate_graph(base_curr: str, targ_curr: str, data: dict, title="") -> str:
    fig, ax = plt.subplots()
    plt.ylabel(f"{base_curr}/{targ_curr}")
    plt.xlabel("dates")
    fig.suptitle(title, fontsize=16)

    dates = []
    values = []
    for key in sorted(data.keys()):
        dates.append(key)
        values.append(data[key])

    ax.plot_date(dates, values, "b-", marker=None)
    ax.grid()
    ax.set_axisbelow(True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    ax.grid(which="major", linestyle="-", linewidth="0.5", color="red")

    filename = f"_media/{uuid4()}.png"
    fig.savefig(filename, papertype="a4", orientation="album", format="png")
    return filename


def history_service(interval, base, symbol, graph_title):
    start_date = str(datetime.date.today() - datetime.timedelta(days=interval))

    is_success, api_message, objects = ExchangeratesAPIHistory()(start_date=start_date, base=base, symbol=symbol)
    if not is_success:
        raise Exception(api_message)

    rates = objects["rates"]
    if not rates:
        return {"error": "currency api service doesn't response"}

    cleaned_data = {}
    for key, value in objects["rates"].items():
        cleaned_data[datetime.datetime.strptime(key, "%Y-%m-%d")] = value[symbol]
    file_name = generate_graph(data=cleaned_data, title=graph_title, targ_curr=symbol, base_curr=base)
    return {"file_name": file_name}
