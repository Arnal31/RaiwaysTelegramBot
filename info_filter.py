def info_filter(info):
    train_list: str = f"‼<b>Поезд:</b>{info.num}‼\n" \
                      f"🚄<b>Имя поезда:</b>{info.way}\n" \
                      f"⏰<b>Дата и время отправления:</b>{info.departure_date} {info.departure_time}\n" \
                      f"⌛<b>Время в пути:</b>{info.time}\n" \
                      f"⏰<b>Дата и время прибытия:</b>{info.arrival_date} {info.arrival_time}\n" \
                      f"💰<b>Цена:</b>💰\n"

    for typing, pricing in info.pricing.items():
        train_list = train_list + f'{typing} : {pricing}\n'

    return train_list
