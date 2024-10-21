\connect central

CREATE TABLE IF NOT EXISTS unknown_devices (
    mac_address varchar(250) NOT NULL,
    last_time varchar(250) NOT NULL,
    PRIMARY KEY (mac_address)
);