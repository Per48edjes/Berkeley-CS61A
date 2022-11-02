(define (cddr s) (cdr (cdr s)))

(define (cadr s)
	(car (cdr s))
)

(define (caddr s)
	(car (cddr s))
)

(define (ascending? asc-lst)
	(if (null? (cdr asc-lst))
		#t
		(and (<= (- (car asc-lst) (car (cdr asc-lst))) 0) (ascending? (cdr asc-lst)))
	)
)

(define (square n) (* n n))

(define (pow base exp)
	(cond
		((or (= base 1) (= exp 0)) (*))
		((odd? exp) (* base (pow base (- exp 1))))
		((even? exp) (square (pow base (/ exp 2))))
	)
)
