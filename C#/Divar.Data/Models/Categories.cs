using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class Categories
    {
        [Key]
        public int Id { get; set; }

        [Display(Name = "نام دسته‌بندی")]
        public string CategoryName { get; set; }

        public virtual IEnumerable<Posts> Posts { get; set; }
    }
}
