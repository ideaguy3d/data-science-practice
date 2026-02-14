class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


# ---------------- Binary Tree ----------------

class BinaryTree:
    def __init__(self):
        self._root = None

    def traverse_in_order(self):
        def helper(node):
            if not node:
                return
            helper(node.left)
            print(node.value)
            helper(node.right)
        helper(self._root)

    def traverse_in_order_iterative(self):
        current = self._root
        stack = []

        while True:
            if current:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                print(current.value)
                current = current.right
            else:
                break

    def traverse_post_order(self):
        def helper(node):
            if not node:
                return
            helper(node.left)
            helper(node.right)
            print(node.value)
        helper(self._root)

    def traverse_post_order_iterative(self):
        if not self._root:
            return

        s1 = [self._root]
        s2 = []

        while s1:
            node = s1.pop()
            s2.append(node)
            if node.left:
                s1.append(node.left)
            if node.right:
                s1.append(node.right)

        while s2:
            print(s2.pop().value)

    def traverse_level_order(self):
        if not self._root:
            return

        queue = [self._root]

        while queue:
            node = queue.pop(0)
            print(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


# ---------------- Binary Search Tree ----------------

class BinarySearchTree:
    def __init__(self):
        self._root = None

    def insert(self, value):
        new_node = Node(value)

        if not self._root:
            self._root = new_node
            return

        current = self._root
        while True:
            if value < current.value:
                if current.left:
                    current = current.left
                else:
                    current.left = new_node
                    break
            elif value > current.value:
                if current.right:
                    current = current.right
                else:
                    current.right = new_node
                    break
            else:
                break

    def find_node(self, value):
        current = self._root
        while current:
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return True
        return False

    def remove(self, value):
        def delete(root, value):
            if not root:
                return None
            if value < root.value:
                root.left = delete(root.left, value)
            elif value > root.value:
                root.right = delete(root.right, value)
            else:
                if not root.left and not root.right:
                    return None
                if not root.left:
                    return root.right
                if not root.right:
                    return root.left
                temp = find_min(root.right)
                root.value = temp.value
                root.right = delete(root.right, temp.value)
            return root

        def find_min(root):
            while root.left:
                root = root.left
            return root

        self._root = delete(self._root, value)


# ---------------- AVL Tree ----------------

class AVLTree(Node):
    def __init__(self, value):
        super().__init__(value)
        self.depth = 1

    def set_depth(self):
        left_depth = self.left.depth if self.left else 0
        right_depth = self.right.depth if self.right else 0
        self.depth = max(left_depth, right_depth) + 1

    def balance_factor(self):
        left_depth = self.left.depth if self.left else 0
        right_depth = self.right.depth if self.right else 0
        return left_depth - right_depth

    def rotate_left(self):
        new_root = self.right
        self.right = new_root.left
        new_root.left = self
        self.set_depth()
        new_root.set_depth()
        return new_root

    def rotate_right(self):
        new_root = self.left
        self.left = new_root.right
        new_root.right = self
        self.set_depth()
        new_root.set_depth()
        return new_root

    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left = self.left.insert(value)
            else:
                self.left = AVLTree(value)
        elif value > self.value:
            if self.right:
                self.right = self.right.insert(value)
            else:
                self.right = AVLTree(value)
        else:
            return self

        self.set_depth()

        balance = self.balance_factor()

        if balance > 1:
            if value > self.left.value:
                self.left = self.left.rotate_left()
            return self.rotate_right()

        if balance < -1:
            if value < self.right.value:
                self.right = self.right.rotate_right()
            return self.rotate_left()

        return self


# ---------------- Utility Functions ----------------

def find_lowest_common_ancestor(root, v1, v2):
    if not root:
        return None
    if max(v1, v2) < root.value:
        return find_lowest_common_ancestor(root.left, v1, v2)
    if min(v1, v2) > root.value:
        return find_lowest_common_ancestor(root.right, v1, v2)
    return root.value


def print_kth_levels(root, k):
    if not root:
        return
    queue = [(root, 0)]
    result = []

    while queue:
        node, level = queue.pop(0)
        if level == k:
            result.append(node.value)
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))

    print(result)


def is_same_tree(r1, r2):
    if not r1 and not r2:
        return True
    if not r1 or not r2:
        return False
    return (
        r1.value == r2.value and
        is_same_tree(r1.left, r2.left) and
        is_same_tree(r1.right, r2.right)
    )


def is_mirror_trees(t1, t2):
    if not t1 and not t2:
        return True
    if not t1 or not t2:
        return False
    return (
        t1.value == t2.value and
        is_mirror_trees(t1.left, t2.right) and
        is_mirror_trees(t1.right, t2.left)
    )
