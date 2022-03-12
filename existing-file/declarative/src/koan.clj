(ns koan
  (:require [clojure.java.io :as io]))

(defn existing [path]
  (if (.exists (io/as-file path))
    path
    (throw (RuntimeException. "DomainError"))))

(defn -main [& args]
  (let [path (first args)]
    (print (slurp (existing path)))))
