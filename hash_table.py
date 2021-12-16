class HashTable:
    def __init__(self, initial_capacity=10):
        self.hash_table = []
        for _ in range(initial_capacity):
            self.hash_table.append([])

    def _get_bucket(self, key):
        key = int(str(key).replace('\xef\xbb\xbf', ''))
        return hash(key) % len(self.hash_table)

    def insert(self, key, item):
        bucket = self._get_bucket(key)
        if self.hash_table[bucket] is None:
            self.hash_table[bucket] = [key, item]
        else:
            for bucket_item in self.hash_table[bucket]:
                if bucket_item[0] == key:
                    bucket_item[1] = [key, item]
                    return
            self.hash_table[bucket].append([key, item])

    def look_up(self, key):
        bucket = self._get_bucket(key)
        bucket_list = self.hash_table[bucket]
        if bucket_list is not None:
            for bucket_item in bucket_list:
                if bucket_item[0] == key:
                    return bucket_item[1]
            return None
        else:
            return None

    def remove(self, key):
        bucket = self._get_bucket(key)
        bucket_list = self.hash_table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)

    def get_count(self):
        count = 0
        for bucket in self.hash_table:
            count += len(bucket)
        return count

    def get_list(self):
        simple_list = []
        for bucket in self.hash_table:
            for item in bucket:
                simple_list.append(item[1])
        return simple_list
