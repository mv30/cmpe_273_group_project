create table execution_detail (
    id serial primary key,
    token varchar(128) unique not null,
    input_provided boolean default FALSE,
    status varchar(128) not null,
    dependencies jsonb );