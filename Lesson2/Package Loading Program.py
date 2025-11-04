max_items = int(input("Provide the number of items to process"))
if max_items <= 0:
    print("Error")
else:
    current_packege_weight = 0
    packages_sent = 0
    total_weight_sent = 0
    unused_capacity_per_package = []
    max_unused_package = None
    max_unused_capacity = 0
    item_count = 0
    max_package_weight = 20

    while item_count < max_items:
        current_weight = int(input("Enter the weight of the item (1 - 10kg) or 0 to quit: "))

        if current_weight == 0:
            print("Terminating the program")
            break

        if 1 <= current_weight <= 10:

            if current_packege_weight + current_weight > max_package_weight:
                print(f"Package sent! Total weight: {current_packege_weight} kg")

                packages_sent += 1
                total_weight_sent += current_packege_weight
                unused_capacity = max_package_weight - current_packege_weight
                unused_capacity_per_package.append(unused_capacity)

                if unused_capacity > max_unused_capacity:
                    max_unused_capacity = unused_capacity
                    max_unused_package = packages_sent

                current_packege_weight = current_weight
            else:
                current_packege_weight += current_weight
            item_count += 1

        else:
            print("Invalid weight! Item must be between 1 and 10 kg.")

    if current_packege_weight > 0:
        print(f"Final package sent! Weight: {current_packege_weight} kg")
        packages_sent += 1
        total_weight_sent += current_packege_weight
        unused_capacity = max_package_weight - current_packege_weight
        unused_capacity_per_package.append(unused_capacity)

        if unused_capacity > max_unused_capacity:
            max_unused_capacity = unused_capacity
            max_unused_package = packages_sent


    print("\n==== SUMMARY ====")
    print(f"Packages sent: {packages_sent}")
    print(f"Total weight sent: {total_weight_sent} kg")

    total_unused = sum(unused_capacity_per_package)
    print(f"Total unused capacity: {total_unused} kg")

    print(f"Package with most unused capacity: {max_unused_package} "
          f"({max_unused_capacity} kg unused)")
      