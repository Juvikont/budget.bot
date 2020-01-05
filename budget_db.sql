create table budget
(
    code_name   varchar(255) primary key,
    daily_limit integer
);

create table categories
(
    code_name       varchar(255) primary key,
    name            varchar(255),
    is_main_expense boolean,
    alias           text
);
create table expense
(
    id primary key,
    sum                integer,
    created            date,
    category_code_name integer,
    message            text,
    FOREIGN KEY (category_code_name) REFERENCES categories (code_name)
);

insert into categories(code_name, name, is_main_expense, alias)
values ('products', 'продукты', true, 'еда'),
       ('coffee & snacks', 'перекусы', true, 'кофе, чай, сендвич, кола, фанта, сникерс'),
       ('dinner', ' обед', true, 'столовая, ланч, бизнес-ланч, бизнес-ланч'),
       ('cafe', 'кафе', true, 'мак, рест, ресторан , макдак, kfc, пиццерия'),
       ('transport', 'общ.транспорт', true, 'автобус, троллейбус, метро'),
       ('taxi', 'такси', false, 'такси, убер, яндекс такси, lyft'),
       ('cell', 'телефон & интернет', true, 'телефон, интурнет, wifi, roaming'),
       ('saas', 'подписки', false, 'yandex.music, подписки, hbo');

insert into budget (code_name, daily_limit)
values ('income', 1000);


