(define-macro
 (if-macro condition if-true if-false)
  `(if ,condition ,if-true ,if-false)
)

(define-macro (or-macro expr1 expr2)
  `(let ((v1 ,expr1))
     (if (not (eq? #f v1)) 
       v1
       ,expr2)
  )
)

(define (replicate x n)
  (if (= n 0) nil
    (cons x (replicate x (- n 1)))
  )
)

; Hmmmm...this still feels janky...
(define-macro (repeat-n expr n)
  `(if (> ,n 1)
    ; ...nested `begins`?
    (begin ,expr (repeat-n ,expr (- ,n 1)))
    ,expr
  )
)

(define (list-of map-expr for var in lst if filter-expr)
  `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst))
)

(define-macro (list-of-macro map-expr for var in lst if filter-expr)
  `(map (lambda (,var) ,map-expr) (filter (lambda (,var) ,filter-expr) ,lst))
)
