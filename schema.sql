drop table if exists nonces;
create table nonces (
  id integer primary key autoincrement,
  'nonce' text not null,
  'payment_instrument_type' text,
  time text default current_timestamp
);
