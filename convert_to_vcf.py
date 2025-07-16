import csv
import datetime

def convert_myheritage_to_vcf(input_csv, output_vcf):
    """
    Converts a MyHeritage raw DNA data file (CSV) to VCF format.

    Args:
        input_csv (str): The path to the input MyHeritage CSV file.
        output_vcf (str): The path to the output VCF file.
    """
    with open(input_csv, 'r') as infile, open(output_vcf, 'w') as outfile:
        # Write VCF header
        outfile.write("##fileformat=VCFv4.2\n")
        outfile.write(f"##fileDate={datetime.date.today().strftime('%Y%m%d')}\n")
        outfile.write("##source=MyHeritageToVCFConverter\n")
        outfile.write("##reference=GRCh37\n")
        for i in range(1, 23):
            outfile.write(f"##contig=<ID={i}>\n")
        outfile.write("##contig=<ID=X>\n")
        outfile.write("##contig=<ID=Y>\n")
        outfile.write("##contig=<ID=MT>\n")
        outfile.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
        outfile.write('##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n')
        outfile.write('##INFO=<ID=RSID,Number=1,Type=String,Description="dbSNP ID">\n')
        outfile.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n")

        csv_reader = csv.reader(infile)
        
        # Skip header lines in CSV
        for row in csv_reader:
            if row[0].startswith('RSID'):
                break

        # Process data rows
        for row in csv_reader:
            rsid, chrom, pos, result = row
            
            # Set dummy values for QUAL and DP since they are not in the source file
            qual = "99"
            dp = "30"
            filter_status = "PASS"
            info = f"DP={dp}"

            if len(result) == 2:
                ref = result[0]
                alt = result[1]
                if ref == alt:
                    alt = '.'
                    gt = '1/1'
                else:
                    gt = '0/1'
            elif len(result) == 1:
                ref = result[0]
                alt = '.'
                gt = '1/.'
            else: # Handle indels or no-calls
                ref = 'N'
                alt = '.'
                gt = './.'


            vcf_line = f"{chrom}\t{pos}\t{rsid}\t{ref}\t{alt}\t{qual}\t{filter_status}\t{info}\tGT\t{gt}\n"
            outfile.write(vcf_line)

if __name__ == "__main__":
    input_file = "raw_dna_data.csv"
    output_file = "dna_data.vcf"
    convert_myheritage_to_vcf(input_file, output_file)
    print(f"Conversion complete. Output written to {output_file}")
