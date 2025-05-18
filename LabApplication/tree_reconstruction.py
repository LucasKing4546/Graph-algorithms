class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        return f"TreeNode({self.val})"

# Average case: O(VlogV)
def build_tree_from_inorder_preorder(inorder, preorder):
    if not inorder or not preorder:
        return None

    inorder_map = {val: idx for idx, val in enumerate(inorder)}

    def build_tree(preorder_start, preorder_end, inorder_start, inorder_end):
        if preorder_start > preorder_end:
            return None

        root_val = preorder[preorder_start]
        root = TreeNode(root_val)

        inorder_root_idx = inorder_map[root_val]

        left_subtree_size = inorder_root_idx - inorder_start

        root.left = build_tree(
            preorder_start + 1,
            preorder_start + left_subtree_size,
            inorder_start,
            inorder_root_idx - 1
        )

        root.right = build_tree(
            preorder_start + left_subtree_size + 1,
            preorder_end,
            inorder_root_idx + 1,
            inorder_end
        )

        return root

    return build_tree(0, len(preorder) - 1, 0, len(inorder) - 1)


def print_tree(root):
    if root is None:
        return

    nodes = [root]
    while nodes:
        current = nodes.pop(0)
        left_val = current.left.val if current.left else "None"
        right_val = current.right.val if current.right else "None"
        print(f"Node: {current.val}, Left: {left_val}, Right: {right_val}")

        if current.left:
            nodes.append(current.left)
        if current.right:
            nodes.append(current.right)


if __name__ == "__main__":
    inorder = [4, 2, 5, 1, 3]
    preorder = [1, 2, 4, 5, 3]

    root = build_tree_from_inorder_preorder(inorder, preorder)
    print("Reconstructed Tree:")
    print_tree(root)