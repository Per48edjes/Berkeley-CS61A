(define-macro (when condition exprs)
  `(if (not ,condition) 
      (quote okay)
      ; I hope this is "intended" usage of `unquote-splicing`, i.e., it "unpacks" a 
      ; list of expressions from its argument, an expression itself)
      (begin ,@exprs)
    )
)

(define-macro (switch expr cases)
  (cons 'cond
        (map (lambda (case)
                        (cons `(eq? ,expr (quote ,(car case))) (cdr case)))
             cases)))
