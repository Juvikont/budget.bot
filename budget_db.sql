create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created date,
    codename integer,
    raw_text text,
    chat_id integer,
    FOREIGN KEY(codename) REFERENCES category(codename)
);

insert into category(codename, name, is_base_expense, aliases)
values ('products', 'продукты', true, 'еда'),
       ('coffee & snacks', 'перекусы', true, 'кофе, чай, сендвич, кола, фанта, сникерс'),
       ('dinner', ' обед', true, 'столовая, ланч, бизнес-ланч, бизнес-ланч'),
       ('cafe', 'кафе', true, 'мак, рест, ресторан , макдак, kfc, пиццерия'),
       ('transport', 'общ.транспорт', true, 'автобус, троллейбус, метро'),
       ('taxi', 'такси', false, 'такси, убер, яндекс такси, lyft'),
       ('cell', 'телефон & интернет', true, 'телефон, интурнет, wifi, roaming'),
       ('saas', 'подписки', false, 'yandex.music, подписки, hbo'),
       ('other', 'прочее',false,'');

insert into budget (codename, daily_limit)
values ('income', 1000);


