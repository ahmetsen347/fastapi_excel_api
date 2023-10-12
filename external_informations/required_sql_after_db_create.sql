-- client table
CREATE  FUNCTION update_date_updated_client()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_updated = now();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_client_date_updated
   BEFORE UPDATE
    ON
        client
    FOR EACH ROW
EXECUTE PROCEDURE update_date_updated_client();

-- client_info table
CREATE  FUNCTION update_date_updated_client_info()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_updated = now();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_client_info_date_updated
   BEFORE UPDATE
    ON
        client_info
    FOR EACH ROW
EXECUTE PROCEDURE update_date_updated_client_info();


-- insurance table
CREATE  FUNCTION update_date_updated_insurance()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_updated = now();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_insurance_date_updated
   BEFORE UPDATE
    ON
        insurance
    FOR EACH ROW
EXECUTE PROCEDURE update_date_updated_insurance();