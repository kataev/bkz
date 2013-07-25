def get_printer_avg_demand(self):
    plugs = self.plug.order_by('date').all()
    values = []
    if len(plugs) > 1:
        for p in plugs:
            v, d = None, None
            if not d and not v:
                d = p.date
                v = p.bill.cartridge.value
            else:
                values.append(v, p.date - d)
    return values
