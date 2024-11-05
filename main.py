import pyodbc
import smtplib
import os
from Connection_Establisher import Connection_Establisher

DB_SERVER = os.environ['PDI_IP']
DB_USERNAME = os.environ['PDI_USER']
DB_PASSWORD = os.environ['PDI_PASSWORD']

# **Email Settings**
SMTP_SERVER = 'your_smtp_server'
SMTP_PORT = 587  # or 465 for SSL
FROM_EMAIL = 'your_email@example.com'
TO_EMAIL = 'recipient_email@example.com'
EMAIL_PASSWORD = 'your_email_password'

def call_stored_procedure(proc_guid):
    connection = Connection_Establisher.Establish_PDI_Connection(Database='PDICompany_1489_01')
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC FI_GetInventoryVariances_SP @SitesProcGUID=?", proc_guid)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return column_names, results

def extract_variance_results(results, column_names):
    variances = {}
    for row in results:
        site_key = row[column_names.index('FuelInvRpt_Site_Key')]
        daily_var = row[column_names.index('FuelInvRpt_DailyStkVar_Exception')]
        cumulative_var = row[column_names.index('FuelInvRpt_CumulativeStkVar_Exception')]
        variances[site_key] = {
            'Daily Variance': daily_var,
            'Cumulative Variance': cumulative_var
        }
    return variances

def send_email(variances):
    msg = MIMEText("Fuel Inventory Variance Report\n")
    msg['Subject'] = "Fuel Inventory Variance Report"
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    for site, vars in variances.items():
        msg.attach(MIMEText(f"Site Key: {site}\n"))
        msg.attach(MIMEText(f"Daily Variance: {vars['Daily Variance']}\n"))
        msg.attach(MIMEText(f"Cumulative Variance: {vars['Cumulative Variance']}\n\n"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(FROM_EMAIL, EMAIL_PASSWORD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

# **Main Execution**
if __name__ == '__main__':
    proc_guid = 'your_procedure_guid'  # replace with the actual GUID
    column_names, results = call_stored_procedure(proc_guid)
   # variances = extract_variance_results(results, column_names)
    #send_email(variances)