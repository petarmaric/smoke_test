import re


class NormalizeWhitespacesMixin(object):
    def normalize_output(self, s):
        return ' '.join(s.split())


class NormalizeToLineEndingNumbersMixin(object):
    FLOAT_RE = re.compile(r'([-+]?[0-9]+\.?[0-9]*)[ \t]*$')

    def normalize_output(self, s):
        normalized_results = []
        for line in s.split('\n'):
            if line.split(): # Skip empty lines
                line = line.replace('\r', '') # Remove '\r' for Windows/*NIX portability
                match = self.FLOAT_RE.search(line)
                if match:
                    normalized_results.append(float(match.group(1)))

        return normalized_results
