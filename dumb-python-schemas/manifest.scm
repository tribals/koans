(import
  (guix profiles)
  (only (gnu packages python) python-3))

(packages->manifest
  (list
    python-3))
