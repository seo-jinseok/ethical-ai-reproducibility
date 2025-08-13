#!/usr/bin/env python3
"""
Outputs Directory File Integrity Verification Script

This script generates and verifies SHA256 checksums for files in the outputs/
directory to ensure file integrity. This is part of the reproducibility
package for the LLM ethical decision-making research project.

Usage:
    python scripts/verify_outputs.py generate  # Generate checksums
    python scripts/verify_outputs.py verify    # Verify checksums
    python scripts/verify_outputs.py status    # Check current status

The script supports various file types including images (PNG, PDF, EPS, SVG),
data files (JSON, CSV, TSV), and documentation (MD, TEX, LOG).
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, Union
from datetime import datetime


class OutputsVerifier:
    """
    File integrity verification class for the outputs directory.
    
    This class provides functionality to generate and verify SHA256 checksums
    for experimental output files, ensuring reproducibility and data integrity
    in the LLM ethical decision-making research.
    """
    
    def __init__(self, outputs_dir: str = "outputs",
                 checksums_file: str = "outputs/checksums.sha256"):
        self.outputs_dir = Path(outputs_dir)
        self.checksums_file = Path(checksums_file)
        
        # Supported file extensions for verification
        self.supported_extensions = {
            '.png', '.pdf', '.eps', '.svg',  # Images
            '.json', '.txt', '.csv', '.tsv',  # Data files
            '.log', '.md', '.tex'  # Documentation
        }
        
        # Create outputs directory if it doesn't exist
        self.outputs_dir.mkdir(exist_ok=True)
    
    def calculate_sha256(self, file_path: Path) -> str:
        """
        Calculate SHA256 hash for a given file.
        
        Args:
            file_path (Path): Path to the file to hash
            
        Returns:
            str: SHA256 hexadecimal digest of the file
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print("❌ Hash calculation error {}: {}".format(
                file_path, e))
            return ""
    
    def get_file_info(self, file_path: Path) -> Dict[str, Union[int, str]]:
        """
        Collect file information including size, modification time, checksum.
        
        Args:
            file_path (Path): Path to the file to analyze
            
        Returns:
            Dict: File information containing size, modified time, and checksum
        """
        try:
            stat = file_path.stat()
            return {
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(
                    stat.st_mtime).isoformat(),
                'checksum': self.calculate_sha256(file_path)
            }
        except Exception as e:
            print("❌ File information collection error {}: {}".format(
                file_path, e))
            return {'size': 0, 'modified': '', 'checksum': ''}
    
    def scan_files(self) -> Dict[str, Dict[str, Union[int, str]]]:
        """
        Scan the outputs directory for supported files.
        
        Returns:
            Dict: Dictionary mapping file paths to their information
        """
        file_info = {}
        total_files = 0
        total_size = 0
        
        print("📁 Scanning: {}".format(self.outputs_dir))
        
        for file_path in self.outputs_dir.rglob('*'):
            if file_path.is_file():
                # Exclude checksum files
                if file_path.name in ['checksums.json', 'checksums.sha256']:
                    continue
                    
                # Process only supported file extensions
                if (file_path.suffix.lower() in self.supported_extensions
                        or file_path.name in ['meta.json',
                                              'make_figs_report.txt']):
                    relative_path = file_path.relative_to(self.outputs_dir)
                    info = self.get_file_info(file_path)
                    
                    if info['checksum']:  # Only if valid checksum exists
                        file_info[str(relative_path)] = info
                        total_files += 1
                        total_size += int(info['size'])
                        print("  ✓ {} ({:,} bytes)".format(
                            relative_path, info['size']))
        
        print("\n📊 Scan completed: {} files, total size: {:,} bytes".format(
            total_files, total_size))
        return file_info
    
    def generate_checksums(self) -> bool:
        """Generate checksum files"""
        print("🔐 Starting checksum generation...")
        
        file_info = self.scan_files()
        
        if not file_info:
            print("❌ No files to verify.")
            return False
        
        try:
            # Save detailed information in JSON format
            checksums_data = {
                'generated_at': datetime.now().isoformat(),
                'total_files': len(file_info),
                'total_size': sum(
                     int(info['size']) for info in file_info.values()),
                'files': file_info
            }
            
            json_file = self.checksums_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(checksums_data, f, indent=2, ensure_ascii=False)
            
            # Also save in traditional SHA256 format
            with open(self.checksums_file, 'w', encoding='utf-8') as f:
                f.write("# Generated at: {}\n".format(
                    checksums_data['generated_at']))
                f.write("# Total files: {}\n".format(
                    checksums_data['total_files']))
                f.write("# Total size: {:,} bytes\n\n".format(
                    checksums_data['total_size']))
                
                for file_path, info in sorted(file_info.items()):
                    f.write("{}  {}\n".format(
                        info['checksum'], file_path))
            
            print("✅ Checksum file generation completed:")
            print("   - {}".format(json_file))
            print("   - {}".format(self.checksums_file))
            return True
            
        except Exception as e:
            print("❌ Checksum file generation failed: {}".format(e))
            return False
    
    def load_checksums(self) -> Dict[str, str]:
        """Load stored checksums"""
        checksums = {}
        
        if not self.checksums_file.exists():
            return checksums
        
        try:
            with open(self.checksums_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('  ', 1)
                        if len(parts) == 2:
                            checksums[parts[1]] = parts[0]
            return checksums
        except Exception as e:
            print("❌ Checksum file loading failed: {}".format(e))
            return {}
    
    def verify_checksums(self) -> bool:
        """Verify checksums"""
        print("🔍 Starting checksum verification...")
        
        stored_checksums = self.load_checksums()
        
        if not stored_checksums:
            print("❌ Checksum file not found: {}".format(
                self.checksums_file))
            print("   Please generate checksums first using 'generate' "
                  "command.")
            return False
        
        current_files = self.scan_files()
        
        # Verification results
        verified = 0
        failed = 0
        missing = 0
        new_files = 0
        
        print("\n🔍 Verification results:")
        
        # Compare stored checksums with current files
        for file_path, expected_checksum in stored_checksums.items():
            if file_path in current_files:
                actual_checksum = current_files[file_path]['checksum']
                if actual_checksum == expected_checksum:
                    print("  ✓ {}".format(file_path))
                    verified += 1
                else:
                    print("  ❌ Checksum mismatch: {} (expected: {}, "
                          "actual: {})".format(
                              file_path, str(expected_checksum)[:8],
                              str(actual_checksum)[:8]))
                    failed += 1
            else:
                print("  ❌ Missing file: {} (checksum: {})"
                      .format(file_path, str(expected_checksum)[:8]))
                missing += 1
        
        # Check for newly added files
        for file_path in current_files:
            if file_path not in stored_checksums:
                checksum = str(current_files[file_path]['checksum'])
                print("  ❌ New file found: {} (checksum: {})"
                      .format(file_path, checksum[:8]))
                new_files += 1
        
        # Summary
        total_expected = len(stored_checksums)
        print("\n📊 Verification summary:")
        print("   Verification success: {} / {}".format(
            verified, total_expected))
        print("   Checksum mismatch: {}".format(failed))
        print("   Missing files: {}".format(missing))
        print("   New files: {}".format(new_files))
        
        success = (failed == 0 and missing == 0 and new_files == 0)
        
        if success:
            print("\n✅ All files have been verified!")
        else:
            print("\n❌ File integrity verification failed!")
            print("   Please update checksums using 'generate' command.")
        
        return success
    
    def show_status(self) -> None:
        """Display current status"""
        print("📋 Outputs directory status")
        print("   Directory: {}".format(self.outputs_dir.absolute()))
        print("   Checksum file: {}".format(
            self.checksums_file.absolute()))
        
        if self.checksums_file.exists():
            stored_checksums = self.load_checksums()
            print("   Stored checksums: {} files".format(
                len(stored_checksums)))
            
            # Checksum file information
            stat = self.checksums_file.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)
            print("   Last updated: {}".format(
                modified.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            print("   Stored checksums: None")
        
        # Scan current files
        current_files = self.scan_files()
        print("   Current files: {}".format(len(current_files)))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Outputs directory file integrity verification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python scripts/verify_outputs.py generate  # Generate checksums
  python scripts/verify_outputs.py verify    # Verify checksums
  python scripts/verify_outputs.py status    # Check status
        """)
    
    parser.add_argument(
        'command',
        choices=['generate', 'verify', 'status'],
        help='Command to execute')
    
    parser.add_argument(
        '--outputs-dir',
        default='outputs',
        help='Directory to verify (default: outputs)')
    
    parser.add_argument(
        '--checksums-file',
        default='outputs/checksums.sha256',
        help='Checksum file path (default: outputs/checksums.sha256)')
    
    args = parser.parse_args()
    
    verifier = OutputsVerifier(
        outputs_dir=args.outputs_dir,
        checksums_file=args.checksums_file
    )
    
    if args.command == 'generate':
        success = verifier.generate_checksums()
        sys.exit(0 if success else 1)
    
    elif args.command == 'verify':
        success = verifier.verify_checksums()
        sys.exit(0 if success else 1)
    
    elif args.command == 'status':
        verifier.show_status()
        sys.exit(0)


if __name__ == '__main__':
    main()