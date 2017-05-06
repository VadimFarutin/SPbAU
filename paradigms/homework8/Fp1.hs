-- 1. head' возвращает первый элемент непустого списка (0,5 балла)
head' :: [a] -> a
head' (x:_) = x
-- 2. tail' возвращает список без первого элемента, для пустого - пустой (0,5)
tail' :: [a] -> [a]
tail' [] = []
tail' (_:x) = x
-- 3. take' возвращает первые n >= 0 элементов исходного списка (0,5)
take' :: Int -> [a] -> [a]
take' n [] = []
take' n (x:xs) = if n == 0 then [] else x:take' (n - 1) xs
-- 4. drop' возвращает список без первых n >= 0 элементов; если n больше длины -- списка, то пустой список. (0,5)
drop' :: Int -> [a] -> [a]
drop' n [] = []
drop' n (x:xs) = if n == 0 then (x:xs) else drop' (n - 1) xs
-- 5. filter' возвращает список из элементов, для которых f возвращает True (0,5)
filter' :: (a -> Bool) -> [a] -> [a]
filter' f xs = [x | x <- xs, f x]
-- 6. foldl' последовательно применяет функцию f к элементу списка l и значению, полученному на предыдущем шаге, начальное значение z (0,5)
-- foldl' (+) 0 [1, 2, 3] == (((0 + 1) + 2) + 3)   
-- foldl' (*) 4 [] == 4
foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x:l) = foldl' f (f z x) l
-- 7. concat' принимает на вход два списка и возвращает их конкатенацию (0,5)
-- concat' [1,2] [3] == [1,2,3]
concat' :: [a] -> [a] -> [a]
concat' [] ys = ys
concat' (x:xs) ys = x:concat' xs ys
-- 8. quickSort' возвращает его отсортированный список (0,5)
quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' xs = concat' (concat' (quickSort' (filter' (< h) xs))
                                 (filter' (== h) xs))
                        (quickSort' (filter' (> h) xs))
				where h = head' xs
