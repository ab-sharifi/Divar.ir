using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Divar.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace Divar.Data.Data
{
    public class DivarDbContext : DbContext
    {
        public DivarDbContext(DbContextOptions<DivarDbContext> options): base(options)
        {
        }

        public DbSet<Users> Users { get; set; }
        public DbSet<Posts> Posts { get; set; }
        public DbSet<States> States { get; set; }
        public DbSet<Cities> Cities { get; set; }
        public DbSet<Categories> Categories { get; set; }
        public DbSet<Notes> Notes { get; set; }
        public DbSet<VisitHistory> VisitHistory { get; set; }
        public DbSet<HistoryLog> HistoryLog { get; set; }
    }
}
