from log_analysis import get_log_file_path_from_cmd_line, filter_log_by_regex
import pandas as pd
import re
import csv

def main():
    log_file = get_log_file_path_from_cmd_line(1)
    dpt_tally = tally_port_traffic(log_file)
    for port, count in dpt_tally.items():
        if count > 100:
            generate_port_traffic_report(log_file, port)
    generate_invalid_user_report(log_file)
    generate_source_ip_log(log_file, '220.195.35.40')


def tally_port_traffic(log_file):
    dest_port_logs = filter_log_by_regex(log_file, 'DPT=(.+?) ')[1]
    port_dict = {}
    for dpt_tup in dest_port_logs:
        dpt_num = dpt_tup[0]
        port_dict[dpt_num] = port_dict.get(dpt_num, 0) + 1
        
    return port_dict

# TODO: Step 9
def generate_port_traffic_report(log_file, port_number):
    regex = r'^(.{6}) (\d\d:\d\d:\d\d).*SRC=(.+?) DST=(.+?) .*SPT=(.+?) DPT=' + f"({port_number})"
    captured_data = filter_log_by_regex(log_file, regex)[1]
    
    report_df = pd.DataFrame(captured_data)
    report_header = ('Date', 'Time', 'Source IP Address', 'Destination IP Address',
                     'Source Port', 'Destination Port')
    report_df.to_csv(f'destination_port_{port_number}_report.csv', index=False, header = report_header)
    return

# TODO: Step 11
def generate_invalid_user_report(log_file):
    regex = r'^(.{6}) (\d\d:\d\d:\d\d).* user (.+?) from (.*)'
    captured_data = filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(captured_data)
    report_header = ('Date', 'Time', 'Username', 'IP Address')
    report_df.to_csv('invalid_users.csv', index=False, header = report_header)
    return

# TODO: Step 12
def generate_source_ip_log(log_file, ip_address):
    regex = r'SRC=' + str(ip_address)
    captured_data = filter_log_by_regex(log_file, regex)[0]
    subbed_address = re.sub('\.', '_', ip_address)
    with open(f'source_ip_{subbed_address}.log', 'w+') as f:
        for line in captured_data:
            f.write('%s' %line)
        f.close()
    return
    #This works but I did not like the spacing
    report_df = pd.DataFrame(captured_data)
    print(report_df)
    report_df.to_csv(f'source_ip_{subbed_address}.log', index=False, header=False, quoting=csv.QUOTE_NONE, escapechar='\\')
    
    return
    

if __name__ == '__main__':
    main()