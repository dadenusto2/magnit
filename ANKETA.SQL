create table anketa( 
    anketa_id int(10) not null auto_increment, 
    last_name varchar(128) not null, 
    first_name varchar(128) not null,
    ot4estvo varchar(128) null, 
    region varchar(128) not null, 
    city varchar(128) not null, 
    phone_number varchar(12) null,
    email varchar(128) null, 
    message varchar(500) not null,
    PRIMARY KEY (anketa_id)
);

create table region(
    region_id int(10) not null auto_increment,
    region varchar(128) not null,
    PRIMARY KEY (region_id)
);

create table cities(
    city_id int(10) not null auto_increment, 
    region_id varchar(128) not null,
    city varchar(128) not null,
    PRIMARY KEY (city_id), 
    FOREIGN KEY (region_id) REFERENCES region (region_id)
);

insert into region(region) values ('Краснодарский край' );
insert into region(region) values ('Ростовская область' );
insert into region(region) values ('Ставропольский край' );

insert into cities(region_id, city) values (1, 'Краснодар' );
insert into cities(region_id, city) values (1, 'Кропоткин' );
insert into cities(region_id, city) values (1, 'Славянск' );
insert into cities(region_id, city) values (2, 'Ростов' );
insert into cities(region_id, city) values (2, 'Шахты' );
insert into cities(region_id, city) values (2, 'Батайск' );
insert into cities(region_id, city) values (3, 'Ставрополь' );
insert into cities(region_id, city) values (3, 'Пятигорск' );
insert into cities(region_id, city) values (3, 'Кисловодск' );
