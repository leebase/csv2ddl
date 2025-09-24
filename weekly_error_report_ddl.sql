CREATE TABLE IF NOT EXISTS Weekly_Error_Report__9_21_25 (
    Date_dt NUMBER(19, 0),
    Demand_Partner_ID NUMBER(5, 0),
    Demand_Partner VARCHAR(34),
    VAST_Error_Code NUMBER(4, 0),
    VAST_Error_Code_Description VARCHAR(102),
    Errors NUMBER(11, 0),
    Timeouts VARCHAR(5)
);