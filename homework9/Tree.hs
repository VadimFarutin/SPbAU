import Prelude hiding (lookup)

-- Реализовать двоичное дерево поиска без балансировки (4 балла)
data BinaryTree k v = Nil | Cons k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” требует, чтобы элементы типа k можно было сравнивать
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup _ Nil = Nothing
lookup x (Cons k v l r) | x == k    = Just v
                        | x < k     = lookup x l
                        | otherwise = lookup x r

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert x y Nil = Cons x y Nil Nil
insert x y (Cons k v l r) | x == k    = Cons x y l r
                          | x < k     = Cons k v (insert x y l) r
                          | otherwise = Cons k v l (insert x y r)

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete x Nil = Nil
delete x (Cons k v l r) | x == k    = merge l r
                        | x < k     = Cons k v (delete x l) r
                        | otherwise = Cons k v l (delete x r)
                        where merge x Nil = x
                              merge x (Cons k v l r) = Cons k v (merge x l) r
