from utils import compute_hash

# ? Reference: https://viblo.asia/p/huong-dan-cai-dat-merkle-trees-XL6lA4jmZek
class MerkleNode:
    def __init__(self, hash: str, data=None) -> None:
        self.parent: MerkleNode = None
        self.left_child: MerkleNode = None
        self.right_child: MerkleNode = None
        self.hash: str = hash
        self.data: str = data

    def print(self) -> None:
        print("Data:", self.data)
        print("Hash:", self.hash)


class MerkleTree:
    def __init__(self, values: list[str]) -> None:
        self.leaves = []

        for value in values:
            node = MerkleNode(compute_hash(value), data=value)
            self.leaves.append(node)

        self.root = self.build_tree(self.leaves)

    def build_tree(self, leaves: list[MerkleNode]) -> MerkleNode:
        num_leaves = len(leaves)

        # Base case: if there is only one leaf node, return it
        if num_leaves == 1:
            return leaves[0]

        # Combine pairs of leaf nodes to create parent nodes
        parents: list[MerkleNode] = []
        for i in range(0, num_leaves, 2):
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child
            parent = self.create_parent(left_child, right_child)
            parents.append(parent)

        # Recursively builds a Merkle tree from the given list of leaf nodes
        return self.build_tree(parents)

    def create_parent(self, left_child: MerkleNode, right_child: MerkleNode) -> MerkleNode:
        # Combine the hash of the left and right child nodes
        combine_hash = compute_hash(left_child.hash + right_child.hash)

        # Create a new parent node
        parent = MerkleNode(
            combine_hash, data=left_child.data + right_child.data)

        # Set the parent node as the parent of the left and right child nodes
        left_child.parent = right_child.parent = parent

        # Set the left and right child nodes as the children of the parent node
        parent.left_child, parent.right_child = left_child, right_child

        # print(f"Left child {left_child.data}: {left_child.hash}")
        # print(f"Right child {right_child.data}: {right_child.hash}")
        # print(f"Parent {parent.data}: {parent.hash}")
        # print()

        return parent

    def get_path(self, data):
        hash = compute_hash(data)

        for leaf in self.leaves:
            if leaf.hash == hash:
                print(f"Leaf {leaf.hash} exist")
                return self.generate_path(leaf)

        return []

    def generate_path(self, node, path=[]):
        if node == self.root:
            path.append(node.hash)
            return path

        is_left = (node.parent.left_child == node)

        if is_left:
             # The second value in the tuple indicates whether the node is a left or right child
            path.append((node.parent.right_child.hash, not is_left))
            return self.generate_path(node.parent, path)
        else:
            path.append((node.parent.left_child.hash, not is_left))
            return self.generate_path(node.parent, path)
        
    def verify_path(self, data, path: list[str]) -> bool:
        if len(path) == 0: return False
        
        sumHash = compute_hash(data)
        
        for hashNode in path[:-1]:
            hash = hashNode[0]
            isLeft = hashNode[1]
            if isLeft:
                sumHash = compute_hash(hash + sumHash)
            else:
                sumHash = compute_hash(sumHash + hash)

        return sumHash == path[-1]



if __name__ == '__main__':
    transactions = ["0", "1", "2", "3", "4", "5", "6", "7"]

    print("Build Merkle tree")
    merkle_tree = MerkleTree(transactions)
    print(f"Root node: {merkle_tree.root.hash}")
    print()
    
    data = "5"
    print(f"Query Merkle path for transaction {data}")
    merkle_path = merkle_tree.get_path(data)
    print(f"Merkle path of {data}: {merkle_path}")
    print()

    print(f"Verify transaction {data}")
    print(merkle_tree.verify_path(data, merkle_path))
    print()

    tampered_data = "50"
    print(f"Test with tampered data {tampered_data}")
    print(merkle_tree.verify_path(tampered_data, merkle_path))
    print()