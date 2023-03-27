(use-modules
  (gnu packages java)
  (guix config)
  (guix profiles))

(define instant
  "60a211ec705ac98483d76da7f2523f2b8966343a")

(let ((moment %guix-version))
  (cond ((equal? instant moment)
         (packages->manifest
          (list
            `(,openjdk11 "jdk"))))
        (else
         (error
          (with-output-to-string
            (lambda ()
              (format #t "Wrong time!~%-~a~%+~a" instant moment)))))))
